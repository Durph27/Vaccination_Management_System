from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Vaccine, VaccineAdministration
from apps.candidates.models import Candidate


@login_required
def vaccine_list(request):
    vaccines = Vaccine.objects.all().order_by('name')
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    if query:
        vaccines = vaccines.filter(name__icontains=query) | Vaccine.objects.filter(manufacturer__icontains=query)
        vaccines = vaccines.distinct()
    if category:
        vaccines = vaccines.filter(target_disease__icontains=category)
    return render(request, 'vaccines/list.html', {
        'vaccines': vaccines,
        'query': query,
        'category': category,
    })


@login_required
def vaccine_detail(request, pk):
    vaccine = get_object_or_404(Vaccine, pk=pk)
    centers = vaccine.vaccinestock_set.select_related('center').filter(quantity__gt=0)
    return render(request, 'vaccines/detail.html', {
        'vaccine': vaccine,
        'centers': centers,
    })


@login_required
def vaccine_history(request):
    """Candidate views their own vaccination history."""
    if not request.user.is_candidate_user():
        return redirect('candidates:dashboard')
    candidate = get_object_or_404(Candidate, user=request.user)
    history = VaccineAdministration.objects.filter(
        appointment__candidate=candidate
    ).select_related('vaccine', 'appointment__center').order_by('-immunization_hour')
    return render(request, 'vaccines/history.html', {'history': history, 'candidate': candidate})


@login_required
def candidate_vaccine_history(request, candidate_pk):
    """Staff views a candidate's vaccination history."""
    if not request.user.is_staff_member():
        return redirect('candidates:dashboard')
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    history = VaccineAdministration.objects.filter(
        appointment__candidate=candidate
    ).select_related('vaccine', 'appointment__center').order_by('-immunization_hour')
    return render(request, 'vaccines/history.html', {'history': history, 'candidate': candidate})
