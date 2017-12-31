from django.db import models
from core.models.base.transactionbase import TransactionBase
from ..master.credit import MCreditCategorySub
from .income import TIncome


class TCredit(TransactionBase):
    """
    Credit Transaction
    """
    amount = models.BigIntegerField()
    m_credit_category_sub = models.ForeignKey(MCreditCategorySub, on_delete=models.CASCADE)
    t_income = models.ForeignKey(TIncome, on_delete=models.CASCADE, related_name='t_credits')
    owner = models.ForeignKey('auth.User', related_name='t_credits', on_delete=models.CASCADE)
