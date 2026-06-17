from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sale
from apps.candidates.models import Candidate


@login_required
def sale_list(request):
    """Staff views all invoices/sales."""
    if not request.user.is_staff_member():
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('candidates:dashboard')

    sales = Sale.objects.select_related(
        'vaccine_administration__appointment__candidate',
    ).prefetch_related(
        'vaccine_administration__vaccines',
    ).order_by('-created_at')
    # SQL: SELECT sl.*, va.dose_number, va.immunization_hour,
    #             a.appointment_date, a.status AS appt_status,
    #             c.full_name AS candidate_name
    #      FROM sales_sale sl
    #      JOIN vaccines_vaccineadministration va ON sl.vaccine_administration_id = va.vaccine_administration_id
    #      JOIN appointments_appointment a ON va.appointment_id = a.appointment_id
    #      JOIN candidates_candidate c ON a.candidate_id = c.candidate_id
    #      ORDER BY sl.created_at DESC

    return render(request, 'sales/list.html', {'sales': sales})


@login_required
def my_sales(request):
    """Candidates view their own paid invoices."""
    if not request.user.is_candidate_user():
        messages.error(request, 'Trang này chỉ dành cho người tiêm.')
        return redirect('candidates:dashboard')

    candidate = get_object_or_404(Candidate, user=request.user)
    # SQL: SELECT * FROM candidates_candidate WHERE user_id = %s LIMIT 1

    sales = Sale.objects.filter(
        vaccine_administration__appointment__candidate=candidate,
        status='paid',
    ).select_related(
        'vaccine_administration__appointment__candidate',
    ).prefetch_related(
        'vaccine_administration__vaccines',
    ).order_by('-created_at')
    # SQL: SELECT sl.*, va.dose_number, va.immunization_hour,
    #             a.appointment_date,
    #             c.full_name AS candidate_name,
    #             v.name AS vaccine_name, v.price
    #      FROM sales_sale sl
    #      JOIN vaccines_vaccineadministration va ON sl.vaccine_administration_id = va.vaccine_administration_id
    #      JOIN appointments_appointment a ON va.appointment_id = a.appointment_id
    #      JOIN candidates_candidate c ON a.candidate_id = c.candidate_id
    #      JOIN vaccines_vaccine v ON va.vaccine_id = v.vaccine_id
    #      WHERE a.candidate_id = %s AND sl.status = 'paid'
    #      ORDER BY sl.created_at DESC

    return render(request, 'sales/my_list.html', {'sales': sales})


@login_required
def sale_detail(request, pk):
    """View details of a single sale/invoice."""
    sale = get_object_or_404(
        Sale.objects.select_related(
            'vaccine_administration__appointment__candidate',
            'vaccine_administration__appointment__center',
            'vaccine_administration__doctor__staff',
            'vaccine_administration__nurse__staff',
        ).prefetch_related(
            'vaccine_administration__vaccines',
        ),
        pk=pk,
    )
    # SQL: SELECT sl.*, va.dose_number, va.immunization_hour, va.notes,
    #             a.appointment_date, a.appointment_time, a.status AS appt_status,
    #             c.full_name AS candidate_name, c.phone,
    #             vc.name AS center_name, vc.address,
    #             ds.name AS doctor_name,
    #             ns.name AS nurse_name
    #      FROM sales_sale sl
    #      JOIN vaccines_vaccineadministration va ON sl.vaccine_administration_id = va.vaccine_administration_id
    #      JOIN appointments_appointment a ON va.appointment_id = a.appointment_id
    #      JOIN candidates_candidate c ON a.candidate_id = c.candidate_id
    #      JOIN appointments_vaccinationcenter vc ON a.center_id = vc.center_id
    #      LEFT JOIN staff_doctor d ON va.doctor_id = d.id
    #      LEFT JOIN staff_staff ds ON d.staff_id = ds.staff_id
    #      LEFT JOIN staff_nurse n ON va.nurse_id = n.id
    #      LEFT JOIN staff_staff ns ON n.staff_id = ns.staff_id
    #      WHERE sl.sale_id = %s
    #      LIMIT 1

    # Candidates can only see their own invoices
    if request.user.is_candidate_user():
        candidate = get_object_or_404(Candidate, user=request.user)
        # SQL: SELECT * FROM candidates_candidate WHERE user_id = %s LIMIT 1

        if sale.vaccine_administration.appointment.candidate != candidate:
            messages.error(request, 'Bạn không có quyền xem hóa đơn này.')
            return redirect('sales:my_sales')
    return render(request, 'sales/detail.html', {'sale': sale})
