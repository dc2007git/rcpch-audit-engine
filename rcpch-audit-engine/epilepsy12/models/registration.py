from dateutil.relativedelta import relativedelta
from datetime import date
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateField
from django.contrib.auth.models import User
import uuid
from ..constants import *
from .time_and_user_mixin import TimeAndUserStampMixin

# other tables
from .hospital_trust import HospitalTrust
from .case import Case
from .site import Site

class Registration(TimeAndUserStampMixin):
    """
    A record is created in the Registration class every time a case is registered for the audit
    A case can be registered only once - TODO Merge Registration with Case class
    """
    registration_uuid=models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        verbose_name="Unique identifier for each registration in the Epilepsy12 audit for a give year."
    )
    registration_date=models.DateField(
        "Date on which registered for the the Epilepsy12 audit"
    )
    locked=models.BooleanField( 
        "Case is locked from further data entry. This occurs automatically if a year has passed since the registration date.", 
        default=False
    )
    locked_at = models.DateTimeField(
        "The date and time at which the registration was locked from further data entry.",
        auto_now_add=True
    )
    locked_by = models.ForeignKey(
        "The user who locked the registration from further data entry.",
        User, 
        on_delete=CASCADE
    )
    closed=models.BooleanField(
        "Case has been closed and will not participate in audit analysis.", 
        default=False
    )
    referring_hospital = models.ForeignKey(
        HospitalTrust, 
        on_delete=CASCADE,
        verbose_name="Name of referring hospital"
    )
    referring_clinician = models.CharField(max_length=50)
    diagnostic_status = models.CharField( # This currently essential - used to exclude nonepilepic kids
        max_length=1,
        choices=DIAGNOSTIC_STATUS,
        verbose_name="Status of epilepsy diagnosis. Must have epilepsy or probable epilepsy to be included."
    )

    # relationships
    case=models.models.ForeignKey(
        Case, 
        on_delete=CASCADE,
        primary_key=True
    )

    site=models.ForeignKey(
        Site, 
        on_delete=CASCADE,
        primary_key=True
    )

    @property
    def close_registration_after_one_year(self):
        # this currently is unlikely to work TODO #19 set locked to true if registered > 1 y
        today = date.today()
        one_year_on = today+relativedelta(years=1)
        if (self.registration_date > one_year_on):
            return True
        else:
            return False


    class Meta:
        ordering = ['registration_date']
        verbose_name = 'Registration',
        verbose_name_plural="Registrations"
        
    
    def __str__(self) -> str:
        return self.registration_date