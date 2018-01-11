from django.db import models
from ..base.userbase import UserBase
from ..master.debt import MDebtCategorySub


class UDebt(UserBase):
    """
    Debt User Model
    """
    name = models.CharField(max_length=30)
    current_principal_amount = models.BigIntegerField()
    current_gained_amount = models.BigIntegerField()
    m_debt_category_sub = models.ForeignKey(MDebtCategorySub, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='debts', on_delete=models.CASCADE)