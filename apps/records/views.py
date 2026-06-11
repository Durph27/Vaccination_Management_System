from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MedicalRecord
from .forms import MedicalRecordForm
from apps.candidates.models import Candidate


@login_required
def my_record(request):
    """Candidates view their own medical record."""
    if not request.user.is_candidate_user():
        messages.error(request, 'Trang này chỉ dành cho người tiêm.')
        return redirect('candidates:dashboard')

    candidate = get_object_or_404(Candidate, user=request.user)
    try:
        medical_record = MedicalRecord.objects.get(candidate=candidate)
    except MedicalRecord.DoesNotExist:
        medical_record = None
    return render(request, 'records/my_record.html', {
        'candidate': candidate,
        'medical_record': medical_record,
    })


@login_required
def edit_record(request, candidate_pk):
    """Doctor/Admin edits a candidate's medical record."""
    if not request.user.is_doctor():
        messages.error(request, 'Chỉ bác sĩ hoặc quản trị viên mới có thể chỉnh sửa hồ sơ y tế.')
        return redirect('candidates:dashboard')

    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    record, created = MedicalRecord.objects.get_or_create(candidate=candidate)
    form = MedicalRecordForm(request.POST or None, instance=record)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Đã cập nhật hồ sơ y tế cho {candidate.full_name}.')
        return redirect('candidates:detail', pk=candidate_pk)
    return render(request, 'records/edit.html', {
        'form': form,
        'candidate': candidate,
        'record': record,
    })
