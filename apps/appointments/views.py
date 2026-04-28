from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, VaccinationCenter
from .forms import AppointmentForm
from apps.candidates.models import Candidate


@login_required
def book_appointment(request):
    if not request.user.is_candidate_user():
        messages.error(request, 'Chức năng này chỉ dành cho người tiêm.')
        return redirect('candidates:dashboard')
    candidate = get_object_or_404(Candidate, user=request.user)
    form = AppointmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        appointment = form.save(commit=False)
        appointment.candidate = candidate
        appointment.save()
        messages.success(request, 'Đặt lịch hẹn thành công! Vui lòng chờ xác nhận.')
        return redirect('candidates:dashboard')
    centers = VaccinationCenter.objects.all()
    return render(request, 'appointments/book.html', {'form': form, 'centers': centers})


@login_required
def my_appointments(request):
    if not request.user.is_candidate_user():
        return redirect('appointments:all_list')
    candidate = get_object_or_404(Candidate, user=request.user)
    appointments = Appointment.objects.filter(candidate=candidate).order_by('-appointment_date')
    return render(request, 'appointments/my_list.html', {'appointments': appointments})


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    # Candidate can only see their own
    if request.user.is_candidate_user():
        candidate = get_object_or_404(Candidate, user=request.user)
        if appointment.candidate != candidate:
            messages.error(request, 'Bạn không có quyền xem lịch hẹn này.')
            return redirect('appointments:my_list')
    return render(request, 'appointments/detail.html', {'appointment': appointment})


@login_required
def cancel_appointment(request, pk):
    if not request.user.is_candidate_user():
        messages.error(request, 'Hành động này chỉ dành cho người tiêm.')
        return redirect('candidates:dashboard')
    candidate = get_object_or_404(Candidate, user=request.user)
    appointment = get_object_or_404(Appointment, pk=pk, candidate=candidate)
    if appointment.status == 'pending':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Đã hủy lịch hẹn.')
    else:
        messages.error(request, 'Không thể hủy lịch hẹn này.')
    return redirect('appointments:my_list')


@login_required
def all_appointments(request):
    """Staff only: view all appointments."""
    if not request.user.is_staff_member():
        return redirect('candidates:dashboard')
    appointments = Appointment.objects.select_related('candidate', 'center').order_by('-appointment_date')
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    return render(request, 'appointments/all_list.html', {
        'appointments': appointments,
        'status_filter': status_filter,
    })


@login_required
def update_appointment_status(request, pk):
    """Staff only: update appointment status."""
    if not request.user.is_staff_member():
        return redirect('candidates:dashboard')
    appointment = get_object_or_404(Appointment, pk=pk)
    new_status = request.POST.get('status')
    if new_status in dict(Appointment.STATUS_CHOICES):
        appointment.status = new_status
        appointment.save()
        messages.success(request, 'Cập nhật trạng thái thành công.')
    return redirect('appointments:detail', pk=pk)
