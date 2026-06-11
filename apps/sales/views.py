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
        'vaccine_administration__vaccine',
    ).order_by('-created_at')
    return render(request, 'sales/list.html', {'sales': sales})


@login_required
def my_sales(request):
    """Candidates view their own paid invoices."""
    if not request.user.is_candidate_user():
        messages.error(request, 'Trang này chỉ dành cho người tiêm.')
        return redirect('candidates:dashboard')

    candidate = get_object_or_404(Candidate, user=request.user)
    sales = Sale.objects.filter(
        vaccine_administration__appointment__candidate=candidate,
        status='paid',
    ).select_related(
        'vaccine_administration__appointment__candidate',
        'vaccine_administration__vaccine',
    ).order_by('-created_at')
    return render(request, 'sales/my_list.html', {'sales': sales})


@login_required
def sale_detail(request, pk):
    """View details of a single sale/invoice."""
    sale = get_object_or_404(
        Sale.objects.select_related(
            'vaccine_administration__appointment__candidate',
            'vaccine_administration__appointment__center',
            'vaccine_administration__vaccine',
            'vaccine_administration__doctor__staff',
            'vaccine_administration__nurse__staff',
        ),
        pk=pk,
    )
    # Candidates can only see their own invoices
    if request.user.is_candidate_user():
        candidate = get_object_or_404(Candidate, user=request.user)
        if sale.vaccine_administration.appointment.candidate != candidate:
            messages.error(request, 'Bạn không có quyền xem hóa đơn này.')
            return redirect('sales:my_sales')
    return render(request, 'sales/detail.html', {'sale': sale})
