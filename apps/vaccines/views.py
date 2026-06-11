from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import Vaccine, VaccineAdministration, VaccineStock
from apps.candidates.models import Candidate
from apps.appointments.models import Appointment
from apps.staff.models import Doctor, Nurse


@login_required
def vaccine_list(request):
    vaccines = Vaccine.objects.annotate(
        total_stock=Sum('vaccinestock__quantity')
    ).order_by('name')
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    if query:
        vaccines = vaccines.filter(name__icontains=query) | Vaccine.objects.annotate(
            total_stock=Sum('vaccinestock__quantity')
        ).filter(manufacturer__icontains=query)
        vaccines = vaccines.distinct()
    if category:
        vaccines = vaccines.filter(target_disease__icontains=category)
    return render(request, 'vaccines/list.html', {
        'vaccines': vaccines,
        'query': query,
        'category': category,
    })


@login_required
def vaccine_detail(request, pk):
    vaccine = get_object_or_404(Vaccine, pk=pk)
    centers = vaccine.vaccinestock_set.select_related('center').filter(quantity__gt=0)
    total_stock = centers.aggregate(total=Sum('quantity'))['total'] or 0
    return render(request, 'vaccines/detail.html', {
        'vaccine': vaccine,
        'centers': centers,
        'total_stock': total_stock,
    })


@login_required
def vaccine_history(request):
    """Candidate views their own vaccination history (only administered ones)."""
    if not request.user.is_candidate_user():
        return redirect('candidates:dashboard')
    candidate = get_object_or_404(Candidate, user=request.user)
    history = VaccineAdministration.objects.filter(
        appointment__candidate=candidate,
        immunization_hour__isnull=False,
    ).select_related('vaccine', 'appointment__center').order_by('-immunization_hour')
    return render(request, 'vaccines/history.html', {'history': history, 'candidate': candidate})


@login_required
def candidate_vaccine_history(request, candidate_pk):
    """Staff views a candidate's vaccination history."""
    if not request.user.is_staff_member():
        return redirect('candidates:dashboard')
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    history = VaccineAdministration.objects.filter(
        appointment__candidate=candidate,
        immunization_hour__isnull=False,
    ).select_related('vaccine', 'appointment__center').order_by('-immunization_hour')
    return render(request, 'vaccines/history.html', {'history': history, 'candidate': candidate})


@login_required
def add_vaccine_administration(request, appointment_pk):
    """Doctor/Admin prescribes a vaccine for a candidate's appointment."""
    if not request.user.is_doctor():
        messages.error(request, 'Chỉ bác sĩ hoặc quản trị viên mới có thể chỉ định vaccine.')
        return redirect('candidates:dashboard')

    appointment = get_object_or_404(Appointment, pk=appointment_pk)
    vaccines = Vaccine.objects.all().order_by('name')

    # Get the doctor profile for the current user (if doctor role)
    doctor_profile = None
    if request.user.role == 'doctor':
        try:
            doctor_profile = Doctor.objects.get(staff__user=request.user)
        except Doctor.DoesNotExist:
            pass
    elif request.user.role == 'admin':
        # Admin can act without a doctor profile
        pass

    if request.method == 'POST':
        vaccine_id = request.POST.get('vaccine')
        dose_number = request.POST.get('dose_number', 1)
        notes = request.POST.get('notes', '')

        if not vaccine_id:
            messages.error(request, 'Vui lòng chọn vaccine.')
        else:
            vaccine = get_object_or_404(Vaccine, pk=vaccine_id)
            VaccineAdministration.objects.create(
                appointment=appointment,
                vaccine=vaccine,
                doctor=doctor_profile,
                dose_number=dose_number,
                notes=notes,
            )
            messages.success(request, f'Đã chỉ định vaccine {vaccine.name} cho {appointment.candidate.full_name}.')
            return redirect('appointments:detail', pk=appointment_pk)

    return render(request, 'vaccines/add_administration.html', {
        'appointment': appointment,
        'vaccines': vaccines,
    })


@login_required
def nurse_update_administration(request, adm_pk):
    """Nurse/Admin updates immunization_hour and post_vaccination_status."""
    if not request.user.is_nurse():
        messages.error(request, 'Chỉ y tá hoặc quản trị viên mới có thể cập nhật thông tin tiêm.')
        return redirect('candidates:dashboard')

    adm = get_object_or_404(VaccineAdministration, pk=adm_pk)

    # Get the nurse profile for the current user
    nurse_profile = None
    if request.user.role == 'nurse':
        try:
            nurse_profile = Nurse.objects.get(staff__user=request.user)
        except Nurse.DoesNotExist:
            pass

    if request.method == 'POST':
        immunization_hour = request.POST.get('immunization_hour')
        post_vaccination_status = request.POST.get('post_vaccination_status', '')

        if not immunization_hour:
            messages.error(request, 'Vui lòng nhập giờ tiêm.')
        else:
            adm.immunization_hour = immunization_hour
            adm.post_vaccination_status = post_vaccination_status
            if nurse_profile:
                adm.nurse = nurse_profile
            adm.save()
            messages.success(request, 'Đã cập nhật thông tin tiêm thành công.')
            return redirect('appointments:detail', pk=adm.appointment.pk)

    return render(request, 'vaccines/nurse_update.html', {'adm': adm})
