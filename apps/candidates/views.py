from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from .models import Candidate
from .forms import CandidateEditForm
from apps.appointments.models import Appointment
from apps.records.models import MedicalRecord
from apps.accounts.models import User


def staff_required(view_func):
    """Decorator: only staff members can access."""
    from functools import wraps
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff_member():
            messages.error(request, 'Bạn không có quyền truy cập trang này.')
            return redirect('candidates:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}

    if user.is_candidate_user():
        candidate = get_object_or_404(Candidate, user=user)
        appointments = Appointment.objects.filter(candidate=candidate).order_by('-appointment_date')[:5]
        try:
            medical_record = MedicalRecord.objects.get(candidate=candidate)
        except MedicalRecord.DoesNotExist:
            medical_record = None
        context.update({
            'candidate': candidate,
            'appointments': appointments,
            'medical_record': medical_record,
            'total_appointments': appointments.count(),
        })
        return render(request, 'dashboard/candidate_dashboard.html', context)
    else:
        # Staff dashboard
        all_appointments = Appointment.objects.order_by('-appointment_date')[:10]
        total_candidates = Candidate.objects.count()
        pending = Appointment.objects.filter(status='pending').count()
        context.update({
            'all_appointments': all_appointments,
            'total_candidates': total_candidates,
            'pending_appointments': pending,
        })
        return render(request, 'dashboard/staff_dashboard.html', context)


@login_required
def my_profile(request):
    candidate = get_object_or_404(Candidate, user=request.user)
    return render(request, 'candidates/profile.html', {'candidate': candidate})


@login_required
@staff_required
def edit_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    form = CandidateEditForm(request.POST or None, instance=candidate)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Đã cập nhật hồ sơ {candidate.full_name}.')
        return redirect('candidates:detail', pk=pk)
    return render(request, 'candidates/edit.html', {'form': form, 'candidate': candidate})


@login_required
@staff_required
def candidate_list(request):
    candidates = Candidate.objects.all().order_by('full_name')
    query = request.GET.get('q', '')
    if query:
        candidates = candidates.filter(full_name__icontains=query)
    return render(request, 'candidates/list.html', {'candidates': candidates, 'query': query})


@login_required
@staff_required
def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    appointments = Appointment.objects.filter(candidate=candidate).order_by('-appointment_date')
    try:
        medical_record = MedicalRecord.objects.get(candidate=candidate)
    except MedicalRecord.DoesNotExist:
        medical_record = None
    return render(request, 'candidates/detail.html', {
        'candidate': candidate,
        'appointments': appointments,
        'medical_record': medical_record,
    })
