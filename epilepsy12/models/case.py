from dateutil import relativedelta
import math
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateField
from django.conf import settings

from epilepsy12.models.hospital_trust import HospitalTrust


from ..constants import *
from ..general_functions import *
from .time_and_user_abstract_base_classes import *


class Case(TimeStampAbstractBaseClass, UserStampAbstractBaseClass):
    """
    This class holds information about each child or young person
    Each case is unique


    For a record to be locked:
    1. all mandatory fields must be complete
    2. NHS number must be present
    3. 1 year must have passed

    """
    # _id = models.ObjectIdField()
    locked = models.BooleanField(  # this determines if the case is locked from editing ? are cases or only registrations locked?
        "Locked",
        default=False,
        blank=True,
        null=True
    )
    locked_at = models.DateTimeField(
        "Date record locked",
        null=True,
        blank=True
    )
    locked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        verbose_name="locked by",
        null=True,
        blank=True
    )
    # nhs_patient = models.BooleanField(
    #     "Is an NHS patient?"
    # )
    nhs_number = models.CharField(  # the NHS number for England and Wales - THIS IS NOT IN THE ORIGINAL TABLES
        "NHS Number",
        max_length=10
        # validators=[MinLengthValidator(  # should be other validation before saving - need to strip out spaces
        #     limit_value=10,
        #     message="The NHS number must be 10 digits long."
        # )]
    )  # TODO #13 NHS Number must be hidden - use case_uuid as proxy
    first_name = CharField(
        "first name",
        max_length=100
    )
    surname = CharField(
        "surname",
        max_length=100
    )
    sex = models.IntegerField(
        choices=SEX_TYPE
    )
    date_of_birth = DateField(
        "date of birth (YYYY-MM-DD)"
    )
    postcode = CharField(
        "postcode",
        max_length=8,
        # validators=[validate_postcode]
    )

    ethnicity = CharField(
        max_length=4,
        choices=ETHNICITIES
    )

    index_of_multiple_deprivation_quintile = models.PositiveSmallIntegerField(
        # this is a calculated field - it relies on the availability of the Deprivare server running
        # A quintile is calculated on save and persisted in the database
        "index of multiple deprivation calculated from MySociety data.",
        blank=True,
        editable=False,
        null=True
    )

    # relationships
    hospital_trusts = models.ManyToManyField(
        HospitalTrust,
        through='Site',
        related_name='cases',
        through_fields=('case', 'hospital_trust')
    )

    @property
    def age(self):
        today = date.today()
        calculated_age = relativedelta.relativedelta(
            today, self.date_of_birth)
        months = calculated_age.months
        years = calculated_age.years
        weeks = calculated_age.weeks
        days = calculated_age.days
        final = ''
        if years == 1:
            final += f'{calculated_age.years} year'
            if (months/12) - years == 1:
                final += f'{months} month'
            elif (months/12)-years > 1:
                final += f'{math.floor((months*12)-years)} months'
            else:
                return final

        elif years > 1:
            final += f'{calculated_age.years} years'
            if (months/12) - years == 1:
                final += f', {months} month'
            elif (months/12)-years > 1:
                final += f', {math.floor((months*12)-years)} months'
            else:
                return final
        else:
            # under a year of age
            if months == 1:
                final += f'{months} month'
            elif months > 0:
                final += f'{months} months, '
                if weeks >= (months*4):
                    if (weeks-(months*4)) == 1:
                        final += '1 week'
                    else:
                        final += f'{math.floor(weeks-(months*4))} weeks'
            else:
                if weeks > 0:
                    if weeks == 1:
                        final += f'{math.floor(weeks)} week'
                    else:
                        final += f'{math.floor(weeks)} weeks'
                else:
                    if days > 0:
                        if days == 1:
                            final += f'{math.floor(days)} day'
                        if days > 1:
                            final += f'{math.floor(days)} days'
                    else:
                        final += 'Happy birthday'
        return final

    def save(
            self,
            *args, **kwargs) -> None:

        # This field requires the deprivare api to be running
        # commented out for now to allow live demo to function
        self.index_of_multiple_deprivation_quintile = imd_for_postcode(
            self.postcode)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        permissions = [
            CAN_VIEW_CHILD_NHS_NUMBER,
            CAN_VIEW_CHILD_DATE_OF_BIRTH,
            CAN_DELETE_CHILD_CASE_DATA,
            CAN_UPDATE_CHILD_CASE_DATA,
            CAN_LOCK_CHILD_CASE_DATA_FROM_EDITING,
            CAN_UNLOCK_CHILD_CASE_DATA_FROM_EDITING,
            CAN_OPT_OUT_CHILD_FROM_INCLUSION_IN_AUDIT,
            CAN_VIEW_CHILD_CASE_DATA,
            CAN_CONSENT_TO_AUDIT_PARTICIPATION
        ]

    def __str__(self) -> str:
        return f'{self.first_name} {self.surname}'
