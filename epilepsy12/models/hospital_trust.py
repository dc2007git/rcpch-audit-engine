from django.db import models
from ..constants import *
from .time_and_user_abstract_base_classes import *


class HospitalTrust(TimeStampAbstractBaseClass, UserStampAbstractBaseClass):
    """
    This class details information about hospital trusts.
    It represents a list of hospital trusts that can be looked up to populate fields in the Site class
    """

    hospital_trust_name = models.CharField(
        max_length=100,
        verbose_name="hospital trust full name"
    )
    # ... any other details about the hospital we need

    class Meta:
        indexes = [models.Index(fields=['hospital_trust_name'])]
        verbose_name = 'hospital trust'
        verbose_name_plural = 'hospital trusts'

    def __str__(self) -> str:
        return self.hospital_trust_name