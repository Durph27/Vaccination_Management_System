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
    # SQL: SELECT * FROM candidates_candidate WHERE user_id = %s LIMIT 1

    try:
        medical_record = MedicalRecord.objects.get(candidate=candidate)
        # SQL: SELECT * FROM records_medicalrecord WHERE candidate_id = %s LIMIT 1
    except MedicalRecord.DoesNotExist:
        medical_record = None
    return render(request, 'records/my_record.html', {
        'candidate': candidate,
        'record': medical_record,       # template uses 'record'
        'medical_record': medical_record,
    })


@login_required
def edit_record(request, candidate_pk):
    """Doctor/Admin edits a candidate's medical record."""
    if not request.user.is_doctor():
        messages.error(request, 'Chỉ bác sĩ hoặc quản trị viên mới có thể chỉnh sửa hồ sơ y tế.')
        return redirect('candidates:dashboard')

    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    # SQL: SELECT * FROM candidates_candidate WHERE candidate_id = %s LIMIT 1

    record, created = MedicalRecord.objects.get_or_create(candidate=candidate)
    # SQL (get): SELECT * FROM records_medicalrecord WHERE candidate_id = %s LIMIT 1
    # SQL (create nếu chưa tồn tại):
    #      INSERT INTO records_medicalrecord
    #      (candidate_id, blood_type, height, weight, allergies, chronic_diseases, notes, created_at, updated_at)
    #      VALUES (%s, '', NULL, NULL, '', '', '', NOW(), NOW())

    form = MedicalRecordForm(request.POST or None, instance=record)
    if request.method == 'POST' and form.is_valid():
        form.save()
        # SQL: UPDATE records_medicalrecord
        #      SET blood_type = %s, height = %s, weight = %s,
        #          allergies = %s, chronic_diseases = %s, notes = %s,
        #          updated_at = NOW()
        #      WHERE record_id = %s

        messages.success(request, f'Đã cập nhật hồ sơ y tế cho {candidate.full_name}.')
        return redirect('candidates:detail', pk=candidate_pk)
    return render(request, 'records/edit.html', {
        'form': form,
        'candidate': candidate,
        'record': record,
    })
