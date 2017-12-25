from django.db import models
from core.models.base.transactionbase import TransactionBase
from ..master.credit import MCreditCategorySub
from .income import TIncome


class TCredit(TransactionBase):
    """
    Credit Transaction
    """
    amount = models.BigIntegerField()
    mCreditCategorySub = models.ForeignKey(MCreditCategorySub,
                                           on_delete=models.CASCADE, related_name='credit_credit_category_sub')
    tIncome = models.ForeignKey(TIncome, on_delete=models.CASCADE, related_name='credits')
