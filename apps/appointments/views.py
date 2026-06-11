import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Appointment, VaccinationCenter
from apps.candidates.models import Candidate


def _get_staff_center(user):
    """Return the center associated with the logged-in staff member, or None for admin."""
    if user.role == 'admin':
        return None  # Admin sees all centers
    try:
        return user.staff_profile.center
    except Exception:
        return None


def _validate_future_datetime(appointment_date_str, appointment_time_str):
    """Return error message string if datetime is not in the future, else None."""
    try:
        appt_date = datetime.date.fromisoformat(appointment_date_str)
        appt_time = datetime.time.fromisoformat(appointment_time_str)
        naive_dt = datetime.datetime.combine(appt_date, appt_time)
        appt_dt = timezone.make_aware(naive_dt)
        if appt_dt <= timezone.now():
            return 'Lịch hẹn phải được đặt vào thời gian trong tương lai.'
    except (ValueError, TypeError):
        return 'Ngày hoặc giờ không hợp lệ.'
    return None


@login_required
def book_appointment(request):
    """Candidates book a new appointment."""
    if not request.user.is_candidate_user():
        messages.error(request, 'Trang này chỉ dành cho người tiêm.')
        return redirect('candidates:dashboard')

    candidate = get_object_or_404(Candidate, user=request.user)
    centers = VaccinationCenter.objects.all().order_by('name')

    if request.method == 'POST':
        center_id = request.POST.get('center')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        notes = request.POST.get('notes', '')

        if not center_id or not appointment_date or not appointment_time:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin.')
        else:
            err = _validate_future_datetime(appointment_date, appointment_time)
            if err:
                messages.error(request, err)
            else:
                center = get_object_or_404(VaccinationCenter, pk=center_id)
                Appointment.objects.create(
                    candidate=candidate,
                    center=center,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    notes=notes,
                )
                messages.success(request, 'Đặt lịch hẹn thành công!')
                return redirect('appointments:my_list')

    return render(request, 'appointments/book.html', {'centers': centers})


@login_required
def my_appointments(request):
    """Candidates view their own appointments."""
    if not request.user.is_candidate_user():
        messages.error(request, 'Trang này chỉ dành cho người tiêm.')
        return redirect('candidates:dashboard')

    candidate = get_object_or_404(Candidate, user=request.user)
    appointments = Appointment.objects.filter(candidate=candidate).order_by('-appointment_date')
    return render(request, 'appointments/my_list.html', {'appointments': appointments})


@login_required
def appointment_detail(request, pk):
    """View detail of a single appointment."""
    appointment = get_object_or_404(Appointment, pk=pk)
    # Candidates can only view their own appointments
    if request.user.is_candidate_user():
        candidate = get_object_or_404(Candidate, user=request.user)
        if appointment.candidate != candidate:
            messages.error(request, 'Bạn không có quyền xem lịch hẹn này.')
            return redirect('appointments:my_list')
    elif not request.user.is_staff_member():
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('candidates:dashboard')
    return render(request, 'appointments/detail.html', {'appointment': appointment})


@login_required
def cancel_appointment(request, pk):
    """Candidates cancel their own pending appointment."""
    if not request.user.is_candidate_user():
        messages.error(request, 'Bạn không có quyền thực hiện hành động này.')
        return redirect('candidates:dashboard')

    candidate = get_object_or_404(Candidate, user=request.user)
    appointment = get_object_or_404(Appointment, pk=pk, candidate=candidate)

    if request.method == 'POST':
        if appointment.status == 'pending':
            appointment.status = 'cancelled'
            appointment.save()
            messages.success(request, 'Đã hủy lịch hẹn thành công.')
        else:
            messages.error(request, 'Chỉ có thể hủy lịch hẹn đang ở trạng thái chờ xác nhận.')
    return redirect('appointments:detail', pk=pk)


@login_required
def all_appointments(request):
    """Staff views appointments — filtered to their center (admin sees all)."""
    if not request.user.is_staff_member():
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('candidates:dashboard')

    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.select_related('candidate', 'center').order_by('-appointment_date')

    # Filter by staff's center (admin sees all)
    staff_center = _get_staff_center(request.user)
    if staff_center:
        appointments = appointments.filter(center=staff_center)

    if status_filter:
        appointments = appointments.filter(status=status_filter)

    return render(request, 'appointments/all_list.html', {
        'appointments': appointments,
        'status_filter': status_filter,
        'staff_center': staff_center,
    })


@login_required
def update_appointment_status(request, pk):
    """Receptionist/Admin: pending→confirmed/waiting_exam/cancelled/paid.
    Doctor/Admin: any status → waiting_injection.
    When set to 'paid', auto-create Sale records.
    """
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status', '')

        # Determine allowed statuses per role
        if request.user.is_receptionist():
            allowed = Appointment.RECEPTIONIST_STATUSES
        elif request.user.is_doctor():
            allowed = Appointment.DOCTOR_STATUSES
        else:
            messages.error(request, 'Bạn không có quyền cập nhật trạng thái lịch hẹn.')
            return redirect('appointments:detail', pk=pk)

        if new_status not in allowed:
            messages.error(request, f'Trạng thái không hợp lệ hoặc bạn không có quyền đặt trạng thái này.')
        else:
            old_status = appointment.status
            appointment.status = new_status
            appointment.save()

            # Auto-create Sale records when status changes to 'paid'
            if new_status == 'paid' and old_status != 'paid':
                _auto_create_sales(appointment)

            messages.success(request, 'Đã cập nhật trạng thái lịch hẹn.')

    return redirect('appointments:detail', pk=pk)


def _auto_create_sales(appointment):
    """Auto-create Sale records for each VaccineAdministration in the appointment."""
    from apps.sales.models import Sale

    administrations = appointment.administrations.all()
    for adm in administrations:
        # Only create if no sale exists yet
        if not hasattr(adm, 'sale'):
            Sale.objects.create(
                vaccine_administration=adm,
                total_amount=adm.vaccine.price,
                payment_method='cash',
                status='paid',
                paid_at=timezone.now(),
            )


@login_required
def receptionist_book_appointment(request, candidate_pk):
    """Receptionist/Admin books an appointment for a candidate."""
    if not request.user.is_receptionist():
        messages.error(request, 'Chỉ lễ tân hoặc quản trị viên mới có thể đặt lịch cho người tiêm.')
        return redirect('candidates:dashboard')

    candidate = get_object_or_404(Candidate, pk=candidate_pk)

    # Receptionist sees only their center; admin sees all
    staff_center = _get_staff_center(request.user)
    if staff_center:
        centers = VaccinationCenter.objects.filter(pk=staff_center.pk)
    else:
        centers = VaccinationCenter.objects.all().order_by('name')

    if request.method == 'POST':
        center_id = request.POST.get('center')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        notes = request.POST.get('notes', '')

        if not center_id or not appointment_date or not appointment_time:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin.')
        else:
            err = _validate_future_datetime(appointment_date, appointment_time)
            if err:
                messages.error(request, err)
            else:
                center = get_object_or_404(VaccinationCenter, pk=center_id)
                appointment = Appointment.objects.create(
                    candidate=candidate,
                    center=center,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    notes=notes,
                    status='confirmed',  # Receptionist-created appointments are auto-confirmed
                )
                messages.success(request, f'Đã đặt lịch hẹn cho {candidate.full_name} thành công!')
                return redirect('appointments:detail', pk=appointment.pk)

    return render(request, 'appointments/receptionist_book.html', {
        'candidate': candidate,
        'centers': centers,
        'staff_center': staff_center,
    })
