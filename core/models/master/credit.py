from django.db import models
from core.models.base.mastarbase import MasterBase


class MCreditCategoryMain(MasterBase):
    """
    Credit Category Main Master
    """
    name = models.CharField(max_length=10)


class MCreditCategorySub(MasterBase):
    """
    Credit Category Sub Master
    """
    name = models.CharField(max_length=30)
    mCreditCategoryMain = models.ForeignKey(MCreditCategoryMain, on_delete=models.CASCADE)