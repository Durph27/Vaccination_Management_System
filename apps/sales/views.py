from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sale
from apps.candidates.models import Candidate


@login_required
def sale_list(request):
    if not request.user.is_staff_member():
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('candidates:dashboard')
    sales = Sale.objects.select_related('vaccine_administration__appointment__candidate').order_by('-created_at')
    return render(request, 'sales/list.html', {'sales': sales})


@login_required
def my_sales(request):
    if not request.user.is_candidate_user():
        return redirect('sales:list')
    candidate = get_object_or_404(Candidate, user=request.user)
    sales = Sale.objects.filter(
        vaccine_administration__appointment__candidate=candidate
    ).order_by('-created_at')
    return render(request, 'sales/my_list.html', {'sales': sales})


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    # Candidates can only view their own sales
    if request.user.is_candidate_user():
        candidate = get_object_or_404(Candidate, user=request.user)
        if sale.vaccine_administration.appointment.candidate != candidate:
            messages.error(request, 'Bạn không có quyền xem hóa đơn này.')
            return redirect('sales:my_sales')
    return render(request, 'sales/detail.html', {'sale': sale})
