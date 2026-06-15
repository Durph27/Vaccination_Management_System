from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Staff


@login_required
def staff_list(request):
    staff = Staff.objects.select_related('user', 'center').all()
    # SQL: SELECT s.*, u.username, u.first_name, u.last_name, u.email, u.role AS user_role,
    #             vc.name AS center_name, vc.address
    #      FROM staff_staff s
    #      JOIN accounts_user u ON s.user_id = u.id
    #      LEFT JOIN appointments_vaccinationcenter vc ON s.center_id = vc.center_id

    return render(request, 'staff/list.html', {'staff': staff})


@login_required
def staff_detail(request, pk):
    member = get_object_or_404(Staff, pk=pk)
    # SQL: SELECT * FROM staff_staff WHERE staff_id = %s LIMIT 1

    return render(request, 'staff/detail.html', {'member': member})
