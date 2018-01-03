from django.db import models
from ..base.userbase import UserBase
from ..master.saifu import MSaifuCategory


class USaifu(UserBase):
    """
    Saifu User Table
    """
    name = models.CharField(max_length=30)
    current_balance = models.BigIntegerField()
    m_saifu_category = models.ForeignKey(MSaifuCategory, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='saifus', on_delete=models.CASCADE)
