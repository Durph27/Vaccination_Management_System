from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Sale
from apps.candidates.models import Candidate


@login_required
def sale_list(request):
    if not request.user.is_staff_member():
        from django.shortcuts import redirect
        return redirect('candidates:dashboard')
    sales = Sale.objects.select_related('vaccine_administration__appointment__candidate').order_by('-created_at')
    return render(request, 'sales/list.html', {'sales': sales})


@login_required
def my_sales(request):
    candidate = get_object_or_404(Candidate, user=request.user)
    sales = Sale.objects.filter(
        vaccine_administration__appointment__candidate=candidate
    ).order_by('-created_at')
    return render(request, 'sales/my_list.html', {'sales': sales})


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/detail.html', {'sale': sale})
