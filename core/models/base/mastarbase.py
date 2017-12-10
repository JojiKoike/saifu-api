from django.db import models


class MasterBase(models.Model):
    """
    Base Model Class for Master
    """
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    class Meta:
        abstract = True
    