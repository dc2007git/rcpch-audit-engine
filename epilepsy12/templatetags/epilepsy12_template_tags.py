from django import template
from django.utils.safestring import mark_safe
from ..general_functions import fetch_concept

register = template.Library()


@register.simple_tag
def percent_complete(registration):
    total = 0
    if registration.audit_progress.initial_assessment_complete:
        total += 12
    if registration.audit_progress.epilepsy_context_complete:
        total += 6
    if registration.audit_progress.multiaxial_diagnosis_complete:
        total += 6
    if registration.audit_progress.assessment_complete:
        total += 16
    if registration.audit_progress.investigations_complete:
        total += 4
    if registration.audit_progress.management_complete:
        total += 4
    return total


@register.simple_tag
def characters_left(description):
    length = 5000-len(description)
    colour = 'black'
    if (length < 10):
        colour = 'red'
    safe_text = f'<span style="color:{colour}">{length}</span>'
    return mark_safe(safe_text)


@register.simple_tag
def percentage_of_total(numerator, denominator):
    if numerator and denominator:
        if (int(denominator) > 0):
            return round(int(numerator)/int(denominator)*100)


@register.filter
def custom_filter(text, color):
    safe_text = '<span style="color:{color}">{text}</span>'.format(
        color=color, text=text)
    return mark_safe(safe_text)


@register.simple_tag
def matches_model_field(field_name, model):
    if field_name:
        value = getattr(model, field_name)
        if value:
            return True
        else:
            return False


@register.filter
def snomed_concept(concept_id):
    concept = fetch_concept(concept_id)
    return concept['preferredDescription']['term']


@register.filter
def is_in(url_name, args):
    """
    receives the request.resolver_match.url_name
    and compares with the template name (can be a list in a string separated by commas),
    returning true if a match is present
    """
    if args is None:
        return None
    arg_list = [arg.strip() for arg in args.split(',')]
    if url_name in arg_list:
        return True
    else:
        return False


@register.filter
def to_class_name(value):
    if value.__class__.__name__ == "Registration":
        return 'Verification/Registration'
    elif value.__class__.__name__ == "InitialAssessment":
        return 'Initial Assessment'
    elif value.__class__.__name__ == "EpilepsyContext":
        return 'Epilepsy Context'
    elif value.__class__.__name__ == "MultiaxialDiagnosis":
        return 'Multiaxial Diagnosis'
    elif value.__class__.__name__ == "Assessment":
        return 'Milestones'
    elif value.__class__.__name__ == "Investigations":
        return 'Investigations'
    elif value.__class__.__name__ == "Management":
        return 'Management'
    elif value.__class__.__name__ == "Site":
        return 'Site'
    elif value.__class__.__name__ == "Episode":
        return 'Episode'
    elif value.__class__.__name__ == "Syndrome":
        return 'Syndrome'
    elif value.__class__.__name__ == "Comorbidity":
        return 'Comorbidity'
    elif value.__class__.__name__ == "Epilepsy12User":
        return 'Epilepsy12 User'
    elif value.__class__.__name__ == "Antiepilepsy Medicine":
        return 'Antiepilepsy Medicine'
    else:
        return 'Error'


@register.filter('has_group')
def has_group(user, group_names_string):
    # thanks to Lucas Simon for this efficiency
    # https://stackoverflow.com/questions/1052531/get-user-group-in-a-template
    """
    Check if user has permission
    """
    result = [x.strip() for x in group_names_string.split(',')]
    groups = user.groups.all().values_list('name', flat=True)
    match = False
    for group in groups:
        if group in result:
            match = True
    return match
