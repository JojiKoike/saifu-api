from django.db import models
from ..base.transactionbase import TransactionBase
from ..user.debt import UDebt


class TDebtGain(TransactionBase):
    """
    Debt Gain Model
    """
    gained_date = models.DateField()
    gained_amount = models.BigIntegerField()
    note = models.TextField()
    u_debt = models.ForeignKey(UDebt, on_delete=models.CASCADE, related_name='t_debt_gains')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='t_debt_gains')
