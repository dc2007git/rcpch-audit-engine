from django.db import models
from django.contrib.auth.models import User
from ..constants import *
from .time_and_user_abstract_base_classes import *


class Investigations(TimeStampAbstractBaseClass, UserStampAbstractBaseClass):
    """
    This class records information about any EEG performed.
    It references the Assessment class as each episode may have optionally have several EEGs.
    """

    eeg_indicated = models.BooleanField(default=True)
    eeg_request_date = models.DateTimeField()
    eeg_performed_date = models.DateTimeField()
    twelve_lead_ecg_status = models.BooleanField(
        default=False
    )
    ct_head_scan_status = models.BooleanField(
        default=False
    )
    mri_brain_date = models.DateField()

    class Meta:
        verbose_name = 'investigations'
        verbose_name_plural = 'investigations'

    def __str__(self) -> str:
        return self.eeg_request_date