from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F
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
    # SQL: SELECT v.*, SUM(vs.quantity) AS total_stock
    #      FROM vaccines_vaccine v
    #      LEFT JOIN vaccines_vaccinestock vs ON vs.vaccine_id = v.vaccine_id
    #      GROUP BY v.vaccine_id
    #      ORDER BY v.name ASC

    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    if query:
        vaccines = vaccines.filter(name__icontains=query) | Vaccine.objects.annotate(
            total_stock=Sum('vaccinestock__quantity')
        ).filter(manufacturer__icontains=query)
        # SQL: ... WHERE v.name LIKE %query% OR v.manufacturer LIKE %query%
        vaccines = vaccines.distinct()
        # SQL: ... (thêm DISTINCT để loại bỏ kết quả trùng lặp)
    if category:
        vaccines = vaccines.filter(target_disease__icontains=category)
        # SQL: ... WHERE v.target_disease LIKE %category%
    return render(request, 'vaccines/list.html', {
        'vaccines': vaccines,
        'query': query,
        'category': category,
    })


@login_required
def vaccine_detail(request, pk):
    vaccine = get_object_or_404(Vaccine, pk=pk)
    # SQL: SELECT * FROM vaccines_vaccine WHERE vaccine_id = %s LIMIT 1

    centers = VaccineStock.objects.select_related('center').filter(vaccine=vaccine, quantity__gt=0)
    # SQL: SELECT vs.*, vc.*
    #      FROM vaccines_vaccinestock vs
    #      JOIN appointments_vaccinationcenter vc ON vs.center_id = vc.center_id
    #      WHERE vs.vaccine_id = %s AND vs.quantity > 0

    total_stock = centers.aggregate(total=Sum('quantity'))['total'] or 0
    # SQL: SELECT SUM(quantity) AS total
    #      FROM vaccines_vaccinestock
    #      WHERE vaccine_id = %s AND quantity > 0

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
    # SQL: SELECT * FROM candidates_candidate WHERE user_id = %s LIMIT 1

    history = VaccineAdministration.objects.filter(
        appointment__candidate=candidate,
        immunization_hour__isnull=False,
    ).select_related('vaccine', 'appointment__center').order_by('-immunization_hour')
    # SQL: SELECT va.*, v.name, v.manufacturer, a.appointment_date, vc.name AS center_name
    #      FROM vaccines_vaccineadministration va
    #      JOIN vaccines_vaccine v ON va.vaccine_id = v.vaccine_id
    #      JOIN appointments_appointment a ON va.appointment_id = a.appointment_id
    #      JOIN appointments_vaccinationcenter vc ON a.center_id = vc.center_id
    #      WHERE a.candidate_id = %s
    #        AND va.immunization_hour IS NOT NULL
    #      ORDER BY va.immunization_hour DESC

    return render(request, 'vaccines/history.html', {'history': history, 'candidate': candidate})


@login_required
def candidate_vaccine_history(request, candidate_pk):
    """Staff views a candidate's vaccination history."""
    if not request.user.is_staff_member():
        return redirect('candidates:dashboard')

    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    # SQL: SELECT * FROM candidates_candidate WHERE candidate_id = %s LIMIT 1

    history = VaccineAdministration.objects.filter(
        appointment__candidate=candidate,
        immunization_hour__isnull=False,
    ).select_related('vaccine', 'appointment__center').order_by('-immunization_hour')
    # SQL: SELECT va.*, v.name, v.manufacturer, a.appointment_date, vc.name AS center_name
    #      FROM vaccines_vaccineadministration va
    #      JOIN vaccines_vaccine v ON va.vaccine_id = v.vaccine_id
    #      JOIN appointments_appointment a ON va.appointment_id = a.appointment_id
    #      JOIN appointments_vaccinationcenter vc ON a.center_id = vc.center_id
    #      WHERE a.candidate_id = %s
    #        AND va.immunization_hour IS NOT NULL
    #      ORDER BY va.immunization_hour DESC

    return render(request, 'vaccines/history.html', {'history': history, 'candidate': candidate})


@login_required
def add_vaccine_administration(request, appointment_pk):
    """Doctor/Admin prescribes a vaccine for a candidate's appointment.
    Only allowed when the appointment is in 'waiting_exam' status.
    """
    if not request.user.is_doctor():
        messages.error(request, 'Chỉ bác sĩ hoặc quản trị viên mới có thể chỉ định vaccine.')
        return redirect('candidates:dashboard')

    appointment = get_object_or_404(Appointment, pk=appointment_pk)
    # SQL: SELECT * FROM appointments_appointment WHERE appointment_id = %s LIMIT 1

    # Doctor can only prescribe for appointments that are in waiting_exam
    if request.user.role != 'admin' and appointment.status != 'waiting_exam':
        messages.error(request, 'Chỉ có thể chỉ định vaccine cho lịch hẹn đang ở trạng thái “Đang chờ khám”.')
        return redirect('appointments:detail', pk=appointment_pk)

    # Center-based access control: non-admin doctors can only work in their own center
    if request.user.role != 'admin':
        try:
            staff_center = request.user.staff_profile.center
        except Exception:
            staff_center = None
        if staff_center and appointment.center != staff_center:
            messages.error(request, 'Bạn chỉ có thể chỉ định vaccine cho lịch hẹn tại cơ sở của bạn.')
            return redirect('appointments:detail', pk=appointment_pk)

    vaccines = Vaccine.objects.all().order_by('name')
    # SQL: SELECT * FROM vaccines_vaccine ORDER BY name ASC

    # Get the doctor profile for the current user (if doctor role)
    doctor_profile = None
    if request.user.role == 'doctor':
        try:
            doctor_profile = Doctor.objects.get(staff__user=request.user)
            # SQL: SELECT d.*
            #      FROM staff_doctor d
            #      JOIN staff_staff s ON d.staff_id = s.staff_id
            #      WHERE s.user_id = %s
            #      LIMIT 1
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
            # SQL: SELECT * FROM vaccines_vaccine WHERE vaccine_id = %s LIMIT 1

            # Check stock at the appointment's center
            try:
                stock = VaccineStock.objects.get(vaccine=vaccine, center=appointment.center)
                # SQL: SELECT * FROM vaccines_vaccinestock
                #      WHERE vaccine_id = %s AND center_id = %s LIMIT 1
            except VaccineStock.DoesNotExist:
                stock = None

            if stock is None or stock.quantity <= 0:
                messages.error(request, f'Vaccine {vaccine.name} đã hết hàng tại trung tâm {appointment.center.name}.')
            else:
                VaccineAdministration.objects.create(
                    appointment=appointment,
                    vaccine=vaccine,
                    doctor=doctor_profile,
                    dose_number=dose_number,
                    notes=notes,
                )
                # SQL: INSERT INTO vaccines_vaccineadministration
                #      (appointment_id, vaccine_id, doctor_id, nurse_id, dose_number, notes,
                #       immunization_hour, post_vaccination_status)
                #      VALUES (%s, %s, %s, NULL, %s, %s, NULL, '')

                # Reduce stock by 1
                stock.quantity = F('quantity') - 1
                stock.save(update_fields=['quantity'])
                # SQL: UPDATE vaccines_vaccinestock
                #      SET quantity = quantity - 1
                #      WHERE id = %s

                messages.success(request, f'Đã chỉ định vaccine {vaccine.name} cho {appointment.candidate.full_name}.')
                return redirect('appointments:detail', pk=appointment_pk)

    return render(request, 'vaccines/add_administration.html', {
        'appointment': appointment,
        'vaccines': vaccines,
    })


@login_required
def nurse_update_administration(request, adm_pk):
    """Nurse/Admin updates immunization_hour and post_vaccination_status.

    Status flow (automatic):
    - If immunization_hour is saved for the first time and appointment is at
      waiting_injection → appointment moves to waiting_observation.
    - If post_vaccination_status is also filled and appointment is at
      waiting_observation → appointment moves to waiting_payment.
    """
    if not request.user.is_nurse():
        messages.error(request, 'Chỉ y tá hoặc quản trị viên mới có thể cập nhật thông tin tiêm.')
        return redirect('candidates:dashboard')

    adm = get_object_or_404(VaccineAdministration, pk=adm_pk)
    # SQL: SELECT * FROM vaccines_vaccineadministration WHERE vaccine_administration_id = %s LIMIT 1

    # Nurse can only update when appointment is waiting_injection or waiting_observation
    if request.user.role != 'admin' and adm.appointment.status not in ('waiting_injection', 'waiting_observation'):
        messages.error(request, 'Chỉ có thể cập nhật thông tin tiêm khi lịch hẹn đang ở trạng thái “Đang chờ tiêm” hoặc “Chờ theo dõi phản ứng”.')
        return redirect('appointments:detail', pk=adm.appointment.pk)

    # Center-based access control: non-admin nurses can only update at their own center
    if request.user.role != 'admin':
        try:
            staff_center = request.user.staff_profile.center
        except Exception:
            staff_center = None
        if staff_center and adm.appointment.center != staff_center:
            messages.error(request, 'Bạn chỉ có thể cập nhật thông tin tiêm tại cơ sở của bạn.')
            return redirect('appointments:detail', pk=adm.appointment.pk)

    # Get the nurse profile for the current user
    nurse_profile = None
    if request.user.role == 'nurse':
        try:
            nurse_profile = Nurse.objects.get(staff__user=request.user)
            # SQL: SELECT n.*
            #      FROM staff_nurse n
            #      JOIN staff_staff s ON n.staff_id = s.staff_id
            #      WHERE s.user_id = %s
            #      LIMIT 1
        except Nurse.DoesNotExist:
            pass

    if request.method == 'POST':
        immunization_hour = request.POST.get('immunization_hour')
        post_vaccination_status = request.POST.get('post_vaccination_status', '').strip()

        if not immunization_hour:
            messages.error(request, 'Vui lòng nhập giờ tiêm.')
        else:
            adm.immunization_hour = immunization_hour
            adm.post_vaccination_status = post_vaccination_status
            if nurse_profile:
                adm.nurse = nurse_profile
            adm.save()
            # SQL: UPDATE vaccines_vaccineadministration
            #      SET immunization_hour = %s,
            #          post_vaccination_status = %s,
            #          nurse_id = %s
            #      WHERE vaccine_administration_id = %s

            # Auto-transition appointment status based on nurse actions
            appt = adm.appointment
            if appt.status == 'waiting_injection':
                # First time nurse records injection hour → move to observation
                appt.status = 'waiting_observation'
                appt.save(update_fields=['status'])
                # SQL: UPDATE appointments_appointment SET status = 'waiting_observation' WHERE appointment_id = %s
                messages.success(request, 'Đã cập nhật giờ tiêm. Lịch hẹn chuyển sang “Chờ theo dõi phản ứng” (30 phút).')
            elif appt.status == 'waiting_observation' and post_vaccination_status:
                # Nurse filled in reaction notes after 30-min observation → move to waiting payment
                appt.status = 'waiting_payment'
                appt.save(update_fields=['status'])
                # SQL: UPDATE appointments_appointment SET status = 'waiting_payment' WHERE appointment_id = %s
                messages.success(request, 'Đã ghi nhận phản ứng sau tiêm. Lịch hẹn chuyển sang “Chờ thanh toán”.')
            else:
                messages.success(request, 'Đã cập nhật thông tin tiêm thành công.')

            return redirect('appointments:detail', pk=adm.appointment.pk)

    return render(request, 'vaccines/nurse_update.html', {'adm': adm})
