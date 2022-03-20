from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from ..models import Registration
from ..models import InitialAssessment
from ..forms_folder import InitialAssessmentForm


@login_required
def create_initial_assessment(request, case_id):
    form = InitialAssessmentForm(request.POST or None)
    registration = Registration.objects.filter(case=case_id).first()
    if request.method == "POST":
        print(form)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.registration = registration
            Registration.objects.filter(case=case_id).update(
                initial_assessment_complete=True)
            obj.save()
            return redirect('cases')
        else:
            print('not valid')

    context = {
        "form": form,
        "case_id": case_id,
        "case_name": registration.case.first_name + " " + registration.case.surname,
        "initial_assessment_complete": registration.initial_assessment_complete,
        "epilepsy_context_complete": registration.epilepsy_context_complete,
        "multiaxial_description_complete": registration.multiaxial_description_complete,
        "investigation_management_complete": registration.investigation_management_complete,
        "active_template": "initial_assessment"
    }
    return render(request=request, template_name='epilepsy12/initial_assessment.html', context=context)


@login_required
def update_initial_assessment(request, case_id):
    initial_assessment = InitialAssessment.objects.filter(
        registration__case=case_id).first()
    registration = Registration.objects.filter(case=case_id).first()
    form = InitialAssessmentForm(instance=initial_assessment)

    if request.method == "POST":
        if ('delete') in request.POST:
            initial_assessment.delete()
            return redirect('cases')
        form = InitialAssessmentForm(request.POST, instance=initial_assessment)
        if form.is_valid:
            obj = form.save()
            obj.save()
            # messages.success(request, "You successfully updated the post")
            return redirect('cases')

    context = {
        "form": form,
        "case_id": case_id,
        "case_name": registration.case.first_name + " " + registration.case.surname,
        "initial_assessment_complete": registration.initial_assessment_complete,
        "epilepsy_context_complete": registration.epilepsy_context_complete,
        "multiaxial_description_complete": registration.multiaxial_description_complete,
        "investigation_management_complete": registration.investigation_management_complete,
        "active_template": "initial_assessment"
    }

    return render(request=request, template_name='epilepsy12/initial_assessment.html', context=context)


@login_required
def delete_initial_assessment(request, id):
    initial_assessment = get_object_or_404(InitialAssessmentForm, id=id)
    initial_assessment.delete()
    return redirect('cases')
