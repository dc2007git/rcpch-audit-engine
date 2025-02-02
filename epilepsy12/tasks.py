# Python Imports
from typing import Literal, Union

# Django Imports
from django.utils.html import strip_tags
from django.core.mail import send_mail, BadHeaderError

# Third party imports
from celery import shared_task, Celery

# E12 Imports
from .general_functions import get_current_cohort_data
from epilepsy12.constants import EnumAbstractionLevel
from epilepsy12.common_view_functions.aggregate_by import update_all_kpi_agg_models

@shared_task
def asynchronously_aggregate_kpis_and_update_models_for_cohort_and_abstraction_level(
    cohort: int = None,
    abstractions: Union[Literal["all"], list[EnumAbstractionLevel]] = "all",
    open_access=False
):
    """This asynchronous task will run through all Cases for the Cohort, for all abstraction levels, aggregate KPI scores and update each abstraction's KPIAggregation model.
    `cohort` and `abstractions` parameters are optional.
    """
    # If no cohort supplied, automatically get cohort from current datetime
    if cohort is None:
        cohort = get_current_cohort_data()["cohort"]

    # By default, this will update all KPIAggregation models for all levels of abstraction
    update_all_kpi_agg_models(cohort=cohort, abstractions=abstractions, open_access=open_access)

@shared_task
def asynchronously_send_email_to_recipients(recipients: list, subject: str, message: str):
    """
    Sends emails
    """
    try:
        send_mail(
            subject=subject,
            from_email="admin@epilepsy12.rcpch.tech",
            recipient_list=recipients,
            fail_silently=False,
            message=strip_tags(message),
            html_message=message,
        )
    except Exception:
        raise BadHeaderError
    
@shared_task
def hello():
    """
    THIS IS A SCHEDULED TASK THAT IS CALLED AT 06:00 EVERY DAY
    THE CRON DATE/FREQUENCY IS SET IN SETTING.PY
    """
    print("Hello Epilepsy12!")
