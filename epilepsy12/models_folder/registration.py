# python
from dateutil.relativedelta import relativedelta
from datetime import datetime
# django
from django.contrib.gis.db import models
# 3rd party
from simple_history.models import HistoricalRecords
# rcpch
from .help_text_mixin import HelpTextMixin
from ..constants import CAN_APPROVE_ELIGIBILITY, CAN_REMOVE_APPROVAL_OF_ELIGIBILITY, CAN_REGISTER_CHILD_IN_EPILEPSY12, CAN_UNREGISTER_CHILD_IN_EPILEPSY12, CAN_CONSENT_TO_AUDIT_PARTICIPATION
from .time_and_user_abstract_base_classes import *
from ..general_functions import nth_tuesday_of_year, cohort_number_from_enrolment_date


class Registration(TimeStampAbstractBaseClass, UserStampAbstractBaseClass, HelpTextMixin):
    """
    A record is created in the Registration class every time a case is registered for the audit
    """

    registration_date = models.DateField(
        help_text={
            'label': "First paediatric assessment",
            'reference': "Setting this date is an irreversible step. Confirmation will be requested to complete this step.",
        },
        null=True,
        default=None
    )

    registration_close_date = models.DateField(
        help_text={
            'label': "First paediatric assessment closing date",
            'reference': "Date on which the registration is due to close",
        },
        default=None,
        null=True
    )

    audit_submission_date = models.DateField(
        help_text={
            'label': "Epilepsy12 submission date",
            'reference': "Date on which the audit submission is due. It is always on the 2nd Tuesday in January.",
        },
        default=None,
        null=True
    )

    def audit_submission_date_calculation(self)->datetime.date:
        """Returns audit submission date.
        
        Defined as registration date + 1 year, and then the first occurring 2nd Tuesday of Jan.

        Returns:
            datetime.date: audit submission date.
        """
        if (self.registration_date):
            
            registration_plus_one_year = self.registration_date + relativedelta(years=1)
            
            second_tuesday_next_year = nth_tuesday_of_year(registration_plus_one_year.year, n=2)
            
            second_tuesday_two_years = nth_tuesday_of_year(registration_plus_one_year.year+1, n=2)
            
            if registration_plus_one_year <= second_tuesday_next_year:
                return second_tuesday_next_year
            else:
                return second_tuesday_two_years
        else:
            return None

    eligibility_criteria_met = models.BooleanField(
        default=None,
        null=True
    )

    cohort = models.PositiveSmallIntegerField(
        default=None,
        null=True
    )

    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.updated_by

    @_history_user.setter
    def _history_user(self, value):
        self.updated_by = value

    def get_current_date(self):
        return datetime.now().date()
    
    @property
    def days_remaining_before_submission(self):
        if self.audit_submission_date:
            today = self.get_current_date()
            remaining_time = self.audit_submission_date - today
            if remaining_time.days < 0:
                return 0
            return remaining_time.days

    # relationships
    case = models.OneToOneField(
        'epilepsy12.Case',
        on_delete=models.PROTECT,
        null=True
    )

    audit_progress = models.OneToOneField(
        'epilepsy12.AuditProgress',
        on_delete=models.CASCADE,
        null=True
    )

    kpi = models.OneToOneField(
        "epilepsy12.KPI",
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'
        permissions = [
            CAN_APPROVE_ELIGIBILITY,
            CAN_REMOVE_APPROVAL_OF_ELIGIBILITY,
            CAN_REGISTER_CHILD_IN_EPILEPSY12,
            CAN_UNREGISTER_CHILD_IN_EPILEPSY12,
            CAN_CONSENT_TO_AUDIT_PARTICIPATION
        ]

    def save(self, *args, **kwargs) -> None:
        if self.registration_date is not None:
            self.registration_close_date = self.registration_date + relativedelta(years=1)
            self.audit_submission_date = self.audit_submission_date_calculation()
            self.cohort = cohort_number_from_enrolment_date(
                self.registration_date)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        if self.registration_date:
            return f'Epilepsy12 registration for {self.case} on {self.registration_date}'
        else:
            return f'Epilepsy12 registration for {self.case} incomplete.'
