from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Candidate
from .forms import CandidateEditForm
from apps.appointments.models import Appointment
from apps.records.models import MedicalRecord
from apps.accounts.models import User
from apps.accounts.forms import RegisterCandidateForm


@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}

    if user.is_candidate_user():
        candidate = get_object_or_404(Candidate, user=user)
        total_appointments = Appointment.objects.filter(candidate=candidate).count()
        appointments = Appointment.objects.filter(candidate=candidate).order_by('-appointment_date')[:5]
        try:
            medical_record = MedicalRecord.objects.get(candidate=candidate)
        except MedicalRecord.DoesNotExist:
            medical_record = None
        context.update({
            'candidate': candidate,
            'appointments': appointments,
            'medical_record': medical_record,
            'total_appointments': total_appointments,
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
    if not request.user.is_candidate_user():
        messages.error(request, 'Trang này chỉ dành cho người tiêm.')
        return redirect('candidates:dashboard')
    candidate = get_object_or_404(Candidate, user=request.user)
    return render(request, 'candidates/profile.html', {'candidate': candidate})


@login_required
def edit_candidate(request, pk):
    """Receptionist/Admin edits a candidate's general profile."""
    if not request.user.is_receptionist():
        messages.error(request, 'Chỉ lễ tân hoặc quản trị viên mới có thể chỉnh sửa hồ sơ người tiêm.')
        return redirect('candidates:dashboard')
    candidate = get_object_or_404(Candidate, pk=pk)
    form = CandidateEditForm(request.POST or None, instance=candidate)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Đã cập nhật hồ sơ {candidate.full_name}.')
        return redirect('candidates:detail', pk=pk)
    return render(request, 'candidates/edit.html', {'form': form, 'candidate': candidate})


@login_required
def candidate_list(request):
    if not request.user.is_staff_member():
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('candidates:dashboard')
    candidates = Candidate.objects.all().order_by('full_name')
    query = request.GET.get('q', '')
    if query:
        candidates = candidates.filter(full_name__icontains=query)
    return render(request, 'candidates/list.html', {'candidates': candidates, 'query': query})


@login_required
def candidate_detail(request, pk):
    if not request.user.is_staff_member():
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('candidates:dashboard')
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


@login_required
def receptionist_create_candidate(request):
    """Receptionist/Admin creates a new candidate account."""
    if not request.user.is_receptionist():
        messages.error(request, 'Chỉ lễ tân hoặc quản trị viên mới có thể tạo tài khoản người tiêm.')
        return redirect('candidates:dashboard')

    form = RegisterCandidateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = User.ROLE_CANDIDATE
        user.save()
        candidate = Candidate.objects.create(
            user=user,
            full_name=user.get_full_name(),
            phone=user.phone,
        )
        messages.success(request, f'Đã tạo tài khoản cho {candidate.full_name} thành công!')
        return redirect('candidates:detail', pk=candidate.pk)
    return render(request, 'candidates/create.html', {'form': form})
