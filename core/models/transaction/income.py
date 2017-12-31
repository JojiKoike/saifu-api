from django.db import models
from core.models.base.transactionbase import TransactionBase
from ..master.income import MIncomeCategorySub
from core.models.user.saifu import USaifu


class TIncome(TransactionBase):
    """
    Income Transaction
    """
    payment_source_name = models.CharField(max_length=30, blank=True, default='')
    income_date = models.DateField()
    note = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='t_incomes', on_delete=models.CASCADE)


class TIncomeDetail(TransactionBase):
    """
    Income Detail Transaction
    """
    t_income = models.ForeignKey(TIncome, on_delete=models.CASCADE, related_name="t_income_details")
    amount = models.BigIntegerField()
    m_income_category_sub = models.ForeignKey(MIncomeCategorySub, on_delete=models.CASCADE)
    u_saifu = models.ForeignKey(USaifu, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='t_income_details', on_delete=models.CASCADE)
