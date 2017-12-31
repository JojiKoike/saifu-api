from django.db import models
from core.models.base.mastarbase import MasterBase


class MSaifuCategory(MasterBase):
    """
    Account Category Master
    """
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
