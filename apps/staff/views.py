from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Staff


@login_required
def staff_list(request):
    staff = Staff.objects.select_related('user', 'center').all()
    return render(request, 'staff/list.html', {'staff': staff})


@login_required
def staff_detail(request, pk):
    member = get_object_or_404(Staff, pk=pk)
    return render(request, 'staff/detail.html', {'member': member})
