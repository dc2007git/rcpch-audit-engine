from operator import itemgetter
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from epilepsy12.constants.causes import AUTOANTIBODIES, EPILEPSY_CAUSES, EPILEPSY_GENE_DEFECTS, EPILEPSY_GENETIC_CAUSE_TYPES, EPILEPSY_STRUCTURAL_CAUSE_TYPES, IMMUNE_CAUSES, METABOLIC_CAUSES
from epilepsy12.constants.semiology import EPILEPSY_SEIZURE_TYPE, EPIS_MISC, MIGRAINES, NON_EPILEPSY_BEHAVIOURAL_ARREST_SYMPTOMS, NON_EPILEPSY_PAROXYSMS, NON_EPILEPSY_SEIZURE_ONSET, NON_EPILEPSY_SEIZURE_TYPE, NON_EPILEPSY_SLEEP_RELATED_SYMPTOMS, NON_EPILEPTIC_SYNCOPES
from epilepsy12.constants.syndromes import SYNDROMES
from epilepsy12.constants.epilepsy_types import EPIL_TYPE_CHOICES, EPILEPSY_DIAGNOSIS_STATUS, EPIS_TYPE
from epilepsy12.models.comorbidity import Comorbidity

from ..general_functions import fuzzy_scan_for_keywords

from ..models import Registration, Keyword, DESSCRIBE

from ..general_functions import *

"""
DESSCRIBE Field lists and supporting functions
"""

FOCAL_EPILEPSY_FIELDS = [
    "experienced_prolonged_focal_seizures",
    "focal_onset_impaired_awareness",
    "focal_onset_automatisms",
    "focal_onset_atonic",
    "focal_onset_clonic",
    "focal_onset_left",
    "focal_onset_right",
    "focal_onset_epileptic_spasms",
    "focal_onset_hyperkinetic",
    "focal_onset_myoclonic",
    "focal_onset_tonic",
    "focal_onset_autonomic",
    "focal_onset_behavioural_arrest",
    "focal_onset_cognitive",
    "focal_onset_emotional",
    "focal_onset_sensory",
    "focal_onset_centrotemporal",
    "focal_onset_temporal",
    "focal_onset_frontal",
    "focal_onset_parietal",
    "focal_onset_occipital",
    "focal_onset_gelastic",
    "focal_onset_focal_to_bilateral_tonic_clonic",
    "focal_onset_other",
    "focal_onset_other_details"
]

GENERALISED_ONSET_EPILEPSY_FIELDS = [
    'prolonged_generalized_convulsive_seizures',
    "epileptic_generalised_onset",
    "epileptic_generalised_onset_other_details",
]

ONSET_NONEPILEPSY = [
    'nonepileptic_seizure_unknown_onset',
    'nonepileptic_seizure_unknown_onset_other_details',
    'nonepileptic_seizure_syncope',
    'nonepileptic_seizure_behavioural',
    'nonepileptic_seizure_sleep',
    'nonepileptic_seizure_paroxysmal',
    'nonepileptic_seizure_migraine',
    'nonepileptic_seizure_miscellaneous',
    'nonepileptic_seizure_other',
]

EPILEPSY_FIELDS = ['were_any_of_the_epileptic_seizures_convulsive'] + \
    FOCAL_EPILEPSY_FIELDS + GENERALISED_ONSET_EPILEPSY_FIELDS
NONEPILEPSY_FIELDS = ONSET_NONEPILEPSY

SEIZURE_CAUSE = [
    'syndrome',
    'seizure_cause_main',
    'seizure_cause_main_snomed_code',
    'seizure_cause_structural',
    'seizure_cause_structural_snomed_code',
    'seizure_cause_genetic',
    'seizure_cause_gene_abnormality',
    'seizure_cause_genetic_other',
    'seizure_cause_gene_abnormality_snomed_code',
    'seizure_cause_chromosomal_abnormality',
    'seizure_cause_infectious',
    'seizure_cause_infectious_snomed_code',
    'seizure_cause_metabolic',
    'seizure_cause_mitochondrial_sctid',
    'seizure_cause_metabolic_other',
    'seizure_cause_metabolic_snomed_code',
    'seizure_cause_immune',
    'seizure_cause_immune_antibody',
    'seizure_cause_immune_antibody_other',
    'seizure_cause_immune_snomed_code',
    'relevant_impairments_behavioural_educational'
]

focal_epilepsy_motor_manifestations = [
    {'name': 'focal_onset_atonic', 'text': "Atonic"},
    {'name': 'focal_onset_clonic', 'text': 'Clonic'},
    {'name': 'focal_onset_epileptic_spasms', 'text': 'Spasms'},
    {'name': 'focal_onset_hyperkinetic', 'text': 'Hyperkinetic'},
    {'name': 'focal_onset_myoclonic', 'text': 'Myoclonic'},
    {'name': 'focal_onset_tonic', 'text': 'Tonic'},
    {'name': 'focal_onset_focal_to_bilateral_tonic_clonic', 'text': 'Tonic-Clonic'},
]
focal_epilepsy_nonmotor_manifestations = [
    {'name': 'focal_onset_automatisms', 'text': 'Automatisms'},
    {'name': 'focal_onset_impaired_awareness', 'text': 'Impaired Awareness'},
    {'name': 'focal_onset_gelastic', 'text': 'Gelastic'},
    {'name': 'focal_onset_autonomic', 'text': 'Autonomic'},
    {'name': 'focal_onset_behavioural_arrest', 'text': 'Behavioural Arrest'},
    {'name': 'focal_onset_cognitive', 'text': 'Cognitive'},
    {'name': 'focal_onset_emotional', 'text': 'Emotional'},
    {'name': 'focal_onset_sensory', 'text': 'Sensory'}
]
focal_epilepsy_eeg_manifestations = [
    {'name': 'focal_onset_centrotemporal', 'text': 'Centrotemporal'},
    {'name': 'focal_onset_temporal', 'text': 'Temporal'},
    {'name': 'focal_onset_frontal', 'text': 'Frontal'},
    {'name': 'focal_onset_parietal', 'text': 'Parietal'},
    {'name': 'focal_onset_occipital', 'text': 'Occipital'},
]
laterality = [
    {'name': 'focal_onset_left', 'text': 'Left'},
    {'name': 'focal_onset_right', 'text': 'Right'}
]

seizure_cause_main_choices = [
    {'name': 'seizure_cause_structural', 'text': 'Structural', 'id': 'Str'},
    {'name': 'seizure_cause_genetic', 'text': 'Genetic', 'id': 'Gen'},
    {'name': 'seizure_cause_infectious', 'text': 'Infectious', 'id': 'Inf'},
    {'name': 'seizure_cause_metabolic', 'text': 'Metabolic', 'id': 'Met'},
    {'name': 'seizure_cause_immune', 'text': 'Immune', 'id': 'Imm'},
    {'name': None, 'text': 'Unknown', 'id': 'NK'},
]

seizure_cause_subtype_choices = [
    {'name': 'seizure_cause_gene_abnormality',
        'text': 'Gene Abnormality', 'id': 'Gen'},
    {'name': 'seizure_cause_immune_antibody', 'text': 'Antibody', 'id': 'Imm'},
]

nonseizure_types = [
    {'name': 'nonepileptic_seizure_syncope',
        'text': 'Syncope And Anoxic Seizures', 'id': 'SAS'},
    {'name': 'nonepileptic_seizure_behavioural',
        'text': 'Behavioral Psychological And Psychiatric Disorders', 'id': 'BPP'},
    {'name': 'nonepileptic_seizure_sleep',
        'text': 'Sleep Related Conditions', 'id': 'SRC'},
    {'name': 'nonepileptic_seizure_paroxysmal',
        'text': 'Paroxysmal Movement Disorders', 'id': 'PMD'},
    {'name': 'nonepileptic_seizure_migraine',
        'text': 'Migraine Associated Disorders', 'id': 'MAD'},
    {'name': 'nonepileptic_seizure_miscellaneous',
        'text': 'Miscellaneous Events', 'id': 'ME'},
    {'name': 'nonepileptic_seizure_other', 'text': 'Other', 'id': 'Oth'}
]


def set_epilepsy_fields_to_none(desscribe_id):
    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)
    DESSCRIBE.objects.filter(registration=desscribe.registration).update(
        were_any_of_the_epileptic_seizures_convulsive=None,
        epileptic_seizure_onset_type=None,
        epileptic_generalised_onset=None,
        epileptic_generalised_onset_other_details=None,
        prolonged_generalized_convulsive_seizures=None,
        focal_onset_impaired_awareness=None,
        focal_onset_automatisms=None,
        focal_onset_atonic=None,
        focal_onset_clonic=None,
        focal_onset_left=None,
        focal_onset_right=None,
        focal_onset_epileptic_spasms=None,
        focal_onset_hyperkinetic=None,
        focal_onset_myoclonic=None,
        focal_onset_tonic=None,
        focal_onset_autonomic=None,
        focal_onset_behavioural_arrest=None,
        focal_onset_cognitive=None,
        focal_onset_emotional=None,
        focal_onset_sensory=None,
        focal_onset_centrotemporal=None,
        focal_onset_temporal=None,
        focal_onset_frontal=None,
        focal_onset_parietal=None,
        focal_onset_occipital=None,
        focal_onset_gelastic=None,
        focal_onset_focal_to_bilateral_tonic_clonic=None,
        focal_onset_other=None,
        focal_onset_other_details=None
    )
    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)


def set_all_nonepilepsy_fields_to_none(desscribe_id: int):
    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)
    DESSCRIBE.objects.filter(registration=desscribe.registration).update(
        nonepileptic_seizure_unknown_onset=None,
        nonepileptic_seizure_unknown_onset_other_details=None,
        nonepileptic_seizure_syncope=None,
        nonepileptic_seizure_behavioural=None,
        nonepileptic_seizure_sleep=None,
        nonepileptic_seizure_paroxysmal=None,
        nonepileptic_seizure_migraine=None,
        nonepileptic_seizure_miscellaneous=None,
        nonepileptic_seizure_other=None
    )


"""
Description fields
"""


@login_required
def edit_description(request, desscribe_id):
    """
    This function is triggered by an htmx post request from the partials/desscribe/description.html form for the desscribe description.
    This component comprises the input free text describing a seizure episode and labels for each of the keywords identified.
    The htmx post request is triggered on every key up.
    This function returns html to the browser.
    TODO #33 implement 5000 character cut off
    """

    description = request.POST.get('description')

    keywords = Keyword.objects.all()
    matched_keywords = fuzzy_scan_for_keywords(description, keywords)

    update_field = {
        'description': description,
        'description_keywords': matched_keywords
    }
    if (len(description) <= 5000):
        DESSCRIBE.objects.update_or_create(
            id=desscribe_id, defaults=update_field)
    desscribe = DESSCRIBE.objects.get(id=desscribe_id)

    context = {
        'desscribe': desscribe
    }

    return render(request, 'epilepsy12/partials/desscribe/description_labels.html', context)


@login_required
def delete_description_keyword(request, desscribe_id, description_keyword_id):
    """
    This function is triggered by an htmx post request from the partials/desscribe/description.html form for the desscribe description_keyword.
    This component comprises the input free text describing a seizure episode and labels for each of the keywords identified.
    The htmx post request is triggered on click of a keyword. It removes that keyword from the saved list.
    This function returns html to the browser.
    """
    description_keyword_list = DESSCRIBE.objects.filter(
        id=desscribe_id).values('description_keywords')
    description_keywords = description_keyword_list[0]['description_keywords']
    del description_keywords[description_keyword_id]

    DESSCRIBE.objects.filter(pk=desscribe_id).update(
        description_keywords=description_keywords)
    desscribe = DESSCRIBE.objects.get(id=desscribe_id)

    context = {
        'desscribe': desscribe
    }

    return render(request, 'epilepsy12/partials/desscribe/description_labels.html', context)


"""
Epilepsy or nonepilepsy
"""


@login_required
def epilepsy_or_nonepilepsy_status(request, desscribe_id):
    """
    Function triggered by a click in the epilepsy_or_nonepilepsy_status partial leading to a post request.
    The desscribe_id is also passed in allowing update of the model.
    Selections for epilepsy set all nonepilepsy related fields to None, and selections for
    nonepilepsy set all epilepsy fields to None. Selections to not known set all 
    selections to none. The epilepsy_or_nonepilepsy_status partial is returned.
    """
    epilepsy_or_nonepilepsy_status = request.htmx.trigger_name

    if epilepsy_or_nonepilepsy_status == 'E':
        # epilepsy selected - set all nonepilepsy to none
        set_epilepsy_fields_to_none(desscribe_id=desscribe_id)
    elif epilepsy_or_nonepilepsy_status == 'NE':
        # nonepilepsy selected - set all epilepsy to none
        set_all_nonepilepsy_fields_to_none(desscribe_id=desscribe_id)
    elif epilepsy_or_nonepilepsy_status == 'NK':
        # notknown selected - set all epilepsy and nonepilepsy to none
        set_epilepsy_fields_to_none(desscribe_id=desscribe_id)
        set_all_nonepilepsy_fields_to_none(desscribe_id=desscribe_id)

    DESSCRIBE.objects.filter(pk=desscribe_id).update(
        epilepsy_or_nonepilepsy_status=epilepsy_or_nonepilepsy_status
    )
    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)

    template = 'epilepsy12/partials/desscribe/epilepsy_or_nonepilepsy_status.html'
    context = {
        "epilepsy_or_nonepilepsy_status_choices": sorted(EPILEPSY_DIAGNOSIS_STATUS, key=itemgetter(1)),
        'epileptic_seizure_onset_types': sorted(EPILEPSY_SEIZURE_TYPE, key=itemgetter(1)),
        'nonepilepsy_onset_types': NON_EPILEPSY_SEIZURE_ONSET,
        'laterality': laterality,
        'focal_epilepsy_motor_manifestations': focal_epilepsy_motor_manifestations,
        'focal_epilepsy_nonmotor_manifestations': focal_epilepsy_nonmotor_manifestations,
        'focal_epilepsy_eeg_manifestations': focal_epilepsy_eeg_manifestations,
        'desscribe': desscribe
    }

    return render(request, template, context)


"""
Epilepsy fields
"""


@login_required
def were_any_of_the_epileptic_seizures_convulsive(request, desscribe_id):
    """
    Post request from multiple choice toggle within epilepsy partial.
    Updates the model and returns the epilepsy partial and parameters
    """

    if request.htmx.trigger_name == 'button-true':
        were_any_of_the_epileptic_seizures_convulsive = True
    elif request.htmx.trigger_name == 'button-false':
        were_any_of_the_epileptic_seizures_convulsive = False
    else:
        were_any_of_the_epileptic_seizures_convulsive = None

    DESSCRIBE.objects.filter(pk=desscribe_id).update(
        were_any_of_the_epileptic_seizures_convulsive=were_any_of_the_epileptic_seizures_convulsive
    )

    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)

    context = {
        'desscribe': desscribe,
        'epileptic_seizure_onset_types': sorted(EPILEPSY_SEIZURE_TYPE, key=itemgetter(1)),
        "epilepsy_or_nonepilepsy_status_choices": sorted(EPILEPSY_DIAGNOSIS_STATUS, key=itemgetter(1)),
        'laterality': laterality,
        'focal_epilepsy_motor_manifestations': focal_epilepsy_motor_manifestations,
        'focal_epilepsy_nonmotor_manifestations': focal_epilepsy_nonmotor_manifestations,
        'focal_epilepsy_eeg_manifestations': focal_epilepsy_eeg_manifestations,
    }

    return render(request=request, template_name='epilepsy12/partials/desscribe/epilepsy.html', context=context)


@login_required
def prolonged_generalized_convulsive_seizures(request, desscribe_id):
    """
    Post request from multiple choice toggle within epilepsy partial.
    Updates the model and returns the epilepsy partial and parameters
    """

    if request.htmx.trigger_name == 'button-true':
        prolonged_generalized_convulsive_seizures = True
    elif request.htmx.trigger_name == 'button-false':
        prolonged_generalized_convulsive_seizures = False
    else:
        prolonged_generalized_convulsive_seizures = None

    DESSCRIBE.objects.filter(pk=desscribe_id).update(
        prolonged_generalized_convulsive_seizures=prolonged_generalized_convulsive_seizures
    )

    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)

    context = {
        'desscribe': desscribe
    }

    return render(request=request, template_name='epilepsy12/partials/desscribe/generalised_onset_epilepsy.html', context=context)


@login_required
def epileptic_seizure_onset_type(request, desscribe_id):
    """
    Defines type of onset if considered to be epilepsy
    Accepts POST request from epilepsy partial and returns the same having
    updated the model with the selection
    If focal onset, sent general onset fields to none, or both 
    to none if not known
    """
    epileptic_seizure_onset_type = request.htmx.trigger_name

    update_fields = {}
    if epileptic_seizure_onset_type == "FO":
        # focal onset - set all generalised onset fields to none
        for field in GENERALISED_ONSET_EPILEPSY_FIELDS:
            update_fields.update({
                field: None
            })
    elif epileptic_seizure_onset_type == "GO":
        # generalised onset - set focal onset fields to none
        for field in FOCAL_EPILEPSY_FIELDS:
            update_fields.update({
                field: None
            })
    else:
        # unknown or unclassified onset. Set all to none
        for field in EPILEPSY_FIELDS:
            update_fields.update({
                field: None
            })

    # update the fields object to include latest selection
    update_fields.update({
        'epileptic_seizure_onset_type': epileptic_seizure_onset_type
    })

    # update the model
    DESSCRIBE.objects.filter(pk=desscribe_id).update(**update_fields)

    # retrieve updated object instance
    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)

    context = {
        'desscribe': desscribe,
        'epileptic_seizure_onset_types': sorted(EPILEPSY_SEIZURE_TYPE, key=itemgetter(1)),
        "epilepsy_or_nonepilepsy_status_choices": sorted(EPILEPSY_DIAGNOSIS_STATUS, key=itemgetter(1)),
        'laterality': laterality,
        'focal_epilepsy_motor_manifestations': focal_epilepsy_motor_manifestations,
        'focal_epilepsy_nonmotor_manifestations': focal_epilepsy_nonmotor_manifestations,
        'focal_epilepsy_eeg_manifestations': focal_epilepsy_eeg_manifestations,
    }

    return render(request=request, template_name='epilepsy12/partials/desscribe/epilepsy.html', context=context)


@login_required
def focal_onset_epilepsy_checked_changed(request, desscribe_id):
    """
    Function triggered by a change in any checkbox/toggle in the focal_onset_epilepsy template leading to a post request.
    The desscribe_id is also passed in allowing update of the model.
    The id of the radio button clicked holds the name of the field in the desscribe model to update
    the name of the radiobutton group clicked holds the name of the list from which to select model fields to update
    """

    if request.htmx.trigger_name == 'focal_epilepsy_motor_manifestations':
        focal_fields = focal_epilepsy_motor_manifestations
    elif request.htmx.trigger_name == 'focal_epilepsy_nonmotor_manifestations':
        focal_fields = focal_epilepsy_nonmotor_manifestations
    elif request.htmx.trigger_name == 'focal_epilepsy_eeg_manifestations':
        focal_fields = focal_epilepsy_eeg_manifestations
    elif request.htmx.trigger_name == 'laterality':
        focal_fields = laterality
    else:
        # TODO this is an error that needs handling
        focal_fields = ()

    update_fields = {}
    for item in focal_fields:
        if request.htmx.trigger == item.get('name'):
            update_fields.update({
                item.get('name'): True
            })
        else:
            update_fields.update({
                item.get('name'): False
            })

    DESSCRIBE.objects.filter(pk=desscribe_id).update(**update_fields)

    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)

    context = {
        'desscribe': desscribe,
        'laterality': laterality,
        'focal_epilepsy_motor_manifestations': focal_epilepsy_motor_manifestations,
        'focal_epilepsy_nonmotor_manifestations': focal_epilepsy_nonmotor_manifestations,
        'focal_epilepsy_eeg_manifestations': focal_epilepsy_eeg_manifestations,
    }

    return render(request=request, template_name="epilepsy12/partials/desscribe/focal_onset_epilepsy.html", context=context)


@login_required
def experienced_prolonged_focal_seizures(request, desscribe_id):
    """
    Post request from multiple choice toggle within epilepsy partial.
    Updates the model and returns the epilepsy partial and parameters
    """

    if request.htmx.trigger_name == 'button-true':
        experienced_prolonged_focal_seizures = True
    elif request.htmx.trigger_name == 'button-false':
        experienced_prolonged_focal_seizures = False
    else:
        experienced_prolonged_focal_seizures = None

    DESSCRIBE.objects.filter(pk=desscribe_id).update(
        experienced_prolonged_focal_seizures=experienced_prolonged_focal_seizures
    )

    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)

    context = {
        'desscribe': desscribe,
        'laterality': laterality,
        'focal_epilepsy_motor_manifestations': focal_epilepsy_motor_manifestations,
        'focal_epilepsy_nonmotor_manifestations': focal_epilepsy_nonmotor_manifestations,
        'focal_epilepsy_eeg_manifestations': focal_epilepsy_eeg_manifestations,
    }

    return render(request=request, template_name="epilepsy12/partials/desscribe/focal_onset_epilepsy.html", context=context)


"""
Nonepilepsy
"""


@login_required
def nonepilepsy_generalised_onset(request, desscribe_id):

    nonepilepsy_generalised_onset = request.htmx.trigger_name
    DESSCRIBE.objects.filter(id=desscribe_id).update(
        nonepileptic_seizure_unknown_onset=nonepilepsy_generalised_onset)
    desscribe = DESSCRIBE.objects.get(id=desscribe_id)

    context = {
        'nonepilepsy_onset_types': NON_EPILEPSY_SEIZURE_ONSET,
        'nonepilepsy_types': sorted(NON_EPILEPSY_SEIZURE_TYPE, key=itemgetter(1)),
        'syncopes': sorted(NON_EPILEPTIC_SYNCOPES, key=itemgetter(1)),
        'behavioural': sorted(NON_EPILEPSY_BEHAVIOURAL_ARREST_SYMPTOMS, key=itemgetter(1)),
        'sleep': sorted(NON_EPILEPSY_SLEEP_RELATED_SYMPTOMS, key=itemgetter(1)),
        'paroxysms': sorted(NON_EPILEPSY_PAROXYSMS, key=itemgetter(1)),
        'migraines': sorted(MIGRAINES, key=itemgetter(1)),
        'nonepilepsy_miscellaneous': sorted(EPIS_MISC, key=itemgetter(1)),
        'desscribe': desscribe
    }

    return render(request, 'epilepsy12/partials/desscribe/nonepilepsy.html', context)


def nonepileptic_seizure_type(request, desscribe_id):
    """
    POST request from select element within nonepilepsy partial
    Returns one of the select options: 
    nonepileptic_seizure_type
    nonepileptic_seizure_syncope
    nonepileptic_seizure_behavioural
    nonepileptic_seizure_sleep
    nonepileptic_seizure_paroxysmal
    nonepileptic_seizure_migraine
    nonepileptic_seizure_miscellaneous

    Updates the nonepileptic_seizure_type and used to filter which subtype is shown
    Returns the same partial with parameters
    """

    update_fields = {
        'nonepileptic_seizure_type': request.POST.get(request.htmx.trigger_name)
    }

    # set any fields that are not this subtype that might have previously been
    # set back to none
    for nonseizure_type in nonseizure_types:
        if nonseizure_type.get('id') is not nonepileptic_seizure_type:
            update_fields.update({
                nonseizure_type.get('name'): None
            })

    DESSCRIBE.objects.filter(pk=desscribe_id).update(
        **update_fields
    )

    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)
    context = {
        'nonepilepsy_onset_types': NON_EPILEPSY_SEIZURE_ONSET,
        'nonepilepsy_types': sorted(NON_EPILEPSY_SEIZURE_TYPE, key=itemgetter(1)),
        'syncopes': sorted(NON_EPILEPTIC_SYNCOPES, key=itemgetter(1)),
        'behavioural': sorted(NON_EPILEPSY_BEHAVIOURAL_ARREST_SYMPTOMS, key=itemgetter(1)),
        'sleep': sorted(NON_EPILEPSY_SLEEP_RELATED_SYMPTOMS, key=itemgetter(1)),
        'paroxysms': sorted(NON_EPILEPSY_PAROXYSMS, key=itemgetter(1)),
        'migraines': sorted(MIGRAINES, key=itemgetter(1)),
        'nonepilepsy_miscellaneous': sorted(EPIS_MISC, key=itemgetter(1)),
        'desscribe': desscribe
    }

    return render(request, 'epilepsy12/partials/desscribe/nonepilepsy.html', context)


def nonepileptic_seizure_subtype(request, desscribe_id):
    """
    POST request from the nonepileptic_seizure_subtype partial select component
    in the nonepilepsy partial
    Returns selection from one of the dropdowns depending on which nonepileptic_seizure_type
    was previously selected
    """
    field_name = request.htmx.trigger_name
    field_selection = request.POST.get(field_name)

    # set selected field to selection, all other nonepilepsy fields to None
    update_fields = {}
    for nonseizure_type in nonseizure_types:
        if nonseizure_type.get('name') == field_name:
            update_fields.update({
                field_name: field_selection
            })
        else:
            update_fields.update({
                nonseizure_type.get('name'): None
            })
    DESSCRIBE.objects.filter(pk=desscribe_id).update(**update_fields)

    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)
    context = {
        'nonepilepsy_onset_types': NON_EPILEPSY_SEIZURE_ONSET,
        'nonepilepsy_types': sorted(NON_EPILEPSY_SEIZURE_TYPE, key=itemgetter(1)),
        'syncopes': sorted(NON_EPILEPTIC_SYNCOPES, key=itemgetter(1)),
        'behavioural': sorted(NON_EPILEPSY_BEHAVIOURAL_ARREST_SYMPTOMS, key=itemgetter(1)),
        'sleep': sorted(NON_EPILEPSY_SLEEP_RELATED_SYMPTOMS, key=itemgetter(1)),
        'paroxysms': sorted(NON_EPILEPSY_PAROXYSMS, key=itemgetter(1)),
        'migraines': sorted(MIGRAINES, key=itemgetter(1)),
        'nonepilepsy_miscellaneous': sorted(EPIS_MISC, key=itemgetter(1)),
        'desscribe': desscribe
    }

    return render(request, 'epilepsy12/partials/desscribe/nonepilepsy.html', context)


"""
Epilepsy Syndromes
"""


@login_required
def syndrome_present(request, desscribe_id):
    """
    POST request from the syndrome partial in the multiaxial_description_form 
    Updates model and returns the syndrome partial
    """
    if request.htmx.trigger_name == 'button-true':
        DESSCRIBE.objects.filter(id=desscribe_id).update(
            syndrome_present=True
        )
    elif request.htmx.trigger_name == 'button-false':
        DESSCRIBE.objects.filter(id=desscribe_id).update(
            syndrome_present=False,
            syndrome=None
        )
    else:
        print("Some mistake happened")
        # TODO need to handle this

    updated_desscribe = DESSCRIBE.objects.get(
        pk=desscribe_id)

    context = {
        "desscribe": updated_desscribe,
        "syndrome_selection": sorted(SYNDROMES, key=itemgetter(1)),
    }

    return render(request=request, template_name='epilepsy12/partials/desscribe/syndrome.html', context=context)


@login_required
def syndrome(request, desscribe_id):
    """
    POST request from the syndrome partial in the multiaxial_description_form 
    Updates model and returns the syndrome partial
    """
    syndrome = request.POST.get('syndrome')

    if syndrome:
        DESSCRIBE.objects.filter(id=desscribe_id).update(
            syndrome=syndrome)
    else:
        return HttpResponse('No dice')

    updated_desscribe = DESSCRIBE.objects.get(
        pk=desscribe_id)

    context = {
        "desscribe": updated_desscribe,
        "syndrome_selection": sorted(SYNDROMES, key=itemgetter(1)),
    }

    return render(request=request, template_name='epilepsy12/partials/desscribe/syndrome.html', context=context)


"""
Seizure causes
"""


@login_required
def seizure_cause_main(request, desscribe_id):
    """
    Post request from multiple choice toggle within 'seizure_cause_main' partial.
    This one of Structural, Infectious, Metabolic, Genetic, Immune, Not Known
    These choices are stored in the EPILEPSY_CHOICES constant list, 
    passed to the template as 'seizure_cause_selection'
    Updates the model, setting other fields to None
    and returns the epilepsy partial and parameters
    """

    seizure_cause_main = request.htmx.trigger_name

    all_fields = seizure_cause_main_choices + seizure_cause_subtype_choices

    update_field = {}
    for field in all_fields:
        if field.get('id') == seizure_cause_main:
            update_field.update({
                'seizure_cause_main': seizure_cause_main
            })
        else:
            if field.get('name'):
                # No Known option has no field
                update_field.update({
                    field.get('name'): None
                })

    # update the model
    DESSCRIBE.objects.filter(pk=desscribe_id).update(
        **update_field)

    # retrieve updated object instance
    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)

    context = {
        "seizure_cause_selection": sorted(EPILEPSY_CAUSES, key=itemgetter(1)),
        'epilepsy_structural_cause_choices': sorted(EPILEPSY_STRUCTURAL_CAUSE_TYPES, key=itemgetter(1)),
        'epilepsy_genetic_cause_choices': sorted(EPILEPSY_GENETIC_CAUSE_TYPES, key=itemgetter(1)),
        'epilepsy_gene_cause_choices': sorted(EPILEPSY_GENE_DEFECTS, key=itemgetter(1)),
        'epilepsy_metabolic_cause_choices': sorted(METABOLIC_CAUSES, key=itemgetter(1)),
        'epilepsy_immune_cause_choices': sorted(IMMUNE_CAUSES, key=itemgetter(1)),
        'epilepsy_autoimmune_antibody_cause_choices': sorted(AUTOANTIBODIES, key=itemgetter(1)),
        'desscribe': desscribe
    }

    return render(request=request, template_name='epilepsy12/partials/desscribe/epilepsy_causes.html', context=context)


def seizure_cause_subtype(request, desscribe_id, subtype):
    """
    POST request from 'seizure_cause_subtype' select
    within seizure_cause_main partial, a different sublist relating to the subtype
    parameter, selected in the 'seizure_cause_main' partial.
    The POST request is triggered by a change in any of the following: 
    seizure_cause_immune, seizure_cause_metabolic and seizure_cause_structural
    Updates the model and returns the epilepsy partial and parameters
    Set to None any unselected types
    """
    subtype_selection = request.POST.get(request.htmx.trigger_name)

    update_fields = {}
    for seizure_cause_main_choice in seizure_cause_main_choices:
        if subtype == seizure_cause_main_choice.get('id'):
            update_fields.update({
                seizure_cause_main_choice.get('name'): subtype_selection
            })
        else:
            if seizure_cause_main_choice.get('name'):
                # unknown option has no field - do not update
                update_fields.update({
                    seizure_cause_main_choice.get('name'): None
                })

    DESSCRIBE.objects.filter(pk=desscribe_id).update(**update_fields)

    # retrieve updated object instance
    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)

    context = {
        "seizure_cause_selection": sorted(EPILEPSY_CAUSES, key=itemgetter(1)),
        'epilepsy_structural_cause_choices': sorted(EPILEPSY_STRUCTURAL_CAUSE_TYPES, key=itemgetter(1)),
        'epilepsy_genetic_cause_choices': sorted(EPILEPSY_GENETIC_CAUSE_TYPES, key=itemgetter(1)),
        'epilepsy_gene_cause_choices': sorted(EPILEPSY_GENE_DEFECTS, key=itemgetter(1)),
        'epilepsy_metabolic_cause_choices': sorted(METABOLIC_CAUSES, key=itemgetter(1)),
        'epilepsy_immune_cause_choices': sorted(IMMUNE_CAUSES, key=itemgetter(1)),
        'epilepsy_autoimmune_antibody_cause_choices': sorted(AUTOANTIBODIES, key=itemgetter(1)),
        'desscribe': desscribe
    }

    return render(request=request, template_name='epilepsy12/partials/desscribe/epilepsy_causes.html', context=context)


def seizure_cause_subtype_subtype(request, desscribe_id):
    """
    POST request from subtype selects in seizure_cause_subtype partial. These include:
    seizure_cause_immune_antibody, seizure_cause_gene_abnormality
    within seizure_cause_main partial.
    Updates the model and returns the epilepsy partial and parameters
    Set to None any unselected types
    """
    field_name = request.htmx.trigger_name
    seizure_cause_subtype_subtype = request.POST.get(field_name)

    update_field = ({
        field_name: seizure_cause_subtype_subtype
    })

    DESSCRIBE.objects.filter(pk=desscribe_id).update(
        **update_field
    )

    # retrieve updated object instance
    desscribe = DESSCRIBE.objects.get(pk=desscribe_id)

    context = {
        "seizure_cause_selection": sorted(EPILEPSY_CAUSES, key=itemgetter(1)),
        'epilepsy_structural_cause_choices': sorted(EPILEPSY_STRUCTURAL_CAUSE_TYPES, key=itemgetter(1)),
        'epilepsy_genetic_cause_choices': sorted(EPILEPSY_GENETIC_CAUSE_TYPES, key=itemgetter(1)),
        'epilepsy_gene_cause_choices': sorted(EPILEPSY_GENE_DEFECTS, key=itemgetter(1)),
        'epilepsy_metabolic_cause_choices': sorted(METABOLIC_CAUSES, key=itemgetter(1)),
        'epilepsy_immune_cause_choices': sorted(IMMUNE_CAUSES, key=itemgetter(1)),
        'epilepsy_autoimmune_antibody_cause_choices': sorted(AUTOANTIBODIES, key=itemgetter(1)),
        'desscribe': desscribe
    }

    return render(request=request, template_name='epilepsy12/partials/desscribe/epilepsy_causes.html', context=context)


"""
RIBE
"""


@login_required
def ribe(request, desscribe_id):

    toggle = request.POST.get('ribe')

    if toggle == 'on':
        toggle = True
    else:
        toggle = False

    desscribe = DESSCRIBE.objects.get(
        pk=desscribe_id)

    registration = desscribe.registration
    case = registration.case
    comorbidities = Comorbidity.objects.filter(case=case)

    if comorbidities.count() > 0:
        toggle = True

    DESSCRIBE.objects.filter(id=desscribe_id).update(
        relevant_impairments_behavioural_educational=toggle)

    updated_desscribe = DESSCRIBE.objects.get(
        pk=desscribe_id)

    context = {
        'desscribe': updated_desscribe,
        'comorbidities': comorbidities,
        'case_id': case.id
    }

    return render(request, "epilepsy12/partials/desscribe/ribe.html", context)


@ login_required
def multiaxial_description(request, case_id):
    """
    """
    registration = Registration.objects.filter(case=case_id).first()
    if DESSCRIBE.objects.filter(registration=registration).exists():
        # there is already a desscribe object for this registration
        desscribe = DESSCRIBE.objects.filter(registration=registration).first()
    else:
        # this is not yet a desscribe object for this description - create one
        desscribe = DESSCRIBE.objects.create(registration=registration)

    choices = Keyword.objects.all()

    context = {
        "desscribe": desscribe,
        "registration": registration,
        "choices": choices,
        "case_id": case_id,
        "epilepsy_or_nonepilepsy_status_choices": sorted(EPILEPSY_DIAGNOSIS_STATUS, key=itemgetter(1)),
        "epileptic_seizure_onset_types": sorted(EPILEPSY_SEIZURE_TYPE, key=itemgetter(1)),
        'laterality': laterality,
        'focal_epilepsy_motor_manifestations': focal_epilepsy_motor_manifestations,
        'focal_epilepsy_nonmotor_manifestations': focal_epilepsy_nonmotor_manifestations,
        'focal_epilepsy_eeg_manifestations': focal_epilepsy_eeg_manifestations,
        "syndrome_selection": sorted(SYNDROMES, key=itemgetter(1)),
        "seizure_cause_selection": sorted(EPILEPSY_CAUSES, key=itemgetter(1)),
        'epilepsy_structural_cause_choices': sorted(EPILEPSY_STRUCTURAL_CAUSE_TYPES, key=itemgetter(1)),
        'epilepsy_genetic_cause_choices': sorted(EPILEPSY_GENETIC_CAUSE_TYPES, key=itemgetter(1)),
        'epilepsy_gene_cause_choices': sorted(EPILEPSY_GENE_DEFECTS, key=itemgetter(1)),
        'epilepsy_metabolic_cause_choices': sorted(METABOLIC_CAUSES, key=itemgetter(1)),
        'epilepsy_immune_cause_choices': sorted(IMMUNE_CAUSES, key=itemgetter(1)),
        'epilepsy_autoimmune_antibody_cause_choices': sorted(AUTOANTIBODIES, key=itemgetter(1)),

        'nonepilepsy_onset_types': NON_EPILEPSY_SEIZURE_ONSET,
        'nonepilepsy_types': sorted(NON_EPILEPSY_SEIZURE_TYPE, key=itemgetter(1)),
        'syncopes': sorted(NON_EPILEPTIC_SYNCOPES, key=itemgetter(1)),
        'behavioural': sorted(NON_EPILEPSY_BEHAVIOURAL_ARREST_SYMPTOMS, key=itemgetter(1)),
        'sleep': sorted(NON_EPILEPSY_SLEEP_RELATED_SYMPTOMS, key=itemgetter(1)),
        'paroxysms': sorted(NON_EPILEPSY_PAROXYSMS, key=itemgetter(1)),
        'migraines': sorted(MIGRAINES, key=itemgetter(1)),
        'nonepilepsy_miscellaneous': sorted(EPIS_MISC, key=itemgetter(1)),

        "registration_complete": registration.audit_progress.registration_complete,
        "initial_assessment_complete": registration.audit_progress.initial_assessment_complete,
        "assessment_complete": registration.audit_progress.assessment_complete,
        "epilepsy_context_complete": registration.audit_progress.epilepsy_context_complete,
        "multiaxial_description_complete": registration.audit_progress.multiaxial_description_complete,
        "investigation_complete": registration.audit_progress.investigation_complete,
        "management_complete": registration.audit_progress.management_complete,
        "active_template": "multiaxial_description"
    }

    return render(request=request, template_name='epilepsy12/multiaxial_description.html', context=context)


def set_all_epilepsy_causes_to_none(except_field):
    set_to_none = {

    }
    if except_field is None:
        set_to_none.update({
            'seizure_cause_main': None,
            'seizure_cause_main_snomed_code': None
        })
    elif except_field != "Str":
        set_to_none.update({
            'seizure_cause_structural': None,
            'seizure_cause_structural_snomed_code': None
        })
    elif except_field != "Gen":
        set_to_none.update({
            'seizure_cause_genetic': None,
            'seizure_cause_gene_abnormality': None,
            'seizure_cause_genetic_other': None,
            'seizure_cause_gene_abnormality_snomed_code': None,
            'seizure_cause_chromosomal_abnormality': None,
        })
    elif except_field != "Inf":
        set_to_none.update({
            'seizure_cause_infectious': None,
            'seizure_cause_infectious_snomed_code': None
        })
    elif except_field != "Met":
        set_to_none.update({
            'seizure_cause_metabolic': None,
            'seizure_cause_metabolic_other': None,
            'seizure_cause_metabolic_snomed_code': None
        })
    elif except_field != "Imm":
        set_to_none.update({
            'seizure_cause_immune': None,
            'seizure_cause_immune_antibody': None,
            'seizure_cause_immune_antibody_other': None
        })
    elif except_field != "NK":
        set_to_none.update({'seizure_cause_immune_snomed_code': None})

    return set_to_none
