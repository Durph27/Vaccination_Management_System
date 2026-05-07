from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, VaccinationCenter
from apps.candidates.models import Candidate


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
    """Staff views all appointments with optional status filter."""
    if not request.user.is_staff_member():
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('candidates:dashboard')

    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.select_related('candidate', 'center').order_by('-appointment_date')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    return render(request, 'appointments/all_list.html', {
        'appointments': appointments,
        'status_filter': status_filter,
    })


@login_required
def update_appointment_status(request, pk):
    """Staff updates the status of an appointment."""
    if not request.user.is_staff_member():
        messages.error(request, 'Bạn không có quyền thực hiện hành động này.')
        return redirect('candidates:dashboard')

    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status', '')
        valid_statuses = [choice[0] for choice in Appointment.STATUS_CHOICES]
        if new_status in valid_statuses:
            appointment.status = new_status
            appointment.save()
            messages.success(request, 'Đã cập nhật trạng thái lịch hẹn.')
        else:
            messages.error(request, 'Trạng thái không hợp lệ.')
    return redirect('appointments:detail', pk=pk)
