from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MedicalRecord
from .forms import MedicalRecordForm
from apps.candidates.models import Candidate


@login_required
def my_record(request):
    if not request.user.is_candidate_user():
        messages.error(request, 'Trang này chỉ dành cho người tiêm.')
        return redirect('candidates:dashboard')
    candidate = get_object_or_404(Candidate, user=request.user)
    try:
        record = MedicalRecord.objects.get(candidate=candidate)
    except MedicalRecord.DoesNotExist:
        record = None
    return render(request, 'records/my_record.html', {'record': record, 'candidate': candidate})


@login_required
def edit_record(request, candidate_pk):
    """Staff only: create or edit medical record."""
    if not request.user.is_staff_member():
        messages.error(request, 'Không có quyền truy cập.')
        return redirect('candidates:dashboard')
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    record, created = MedicalRecord.objects.get_or_create(candidate=candidate)
    form = MedicalRecordForm(request.POST or None, instance=record)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Đã cập nhật hồ sơ y tế.')
        return redirect('candidates:detail', pk=candidate_pk)
    return render(request, 'records/edit.html', {'form': form, 'candidate': candidate})
