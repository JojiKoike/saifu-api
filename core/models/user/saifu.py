from django.db import models
from ..base.userbase import UserBase
from ..master.saifu import MSaifuCategorySub


class USaifu(UserBase):
    """
    Saifu User Table
    """
    name = models.CharField(max_length=30)
    current_balance = models.BigIntegerField()
    m_saifu_category_sub = models.ForeignKey(MSaifuCategorySub, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='saifus', on_delete=models.CASCADE)
