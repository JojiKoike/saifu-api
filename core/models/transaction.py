from django.db import models
from .base.transactionbase import TransactionBase
from .master import MasterExpenseCategorySub, MasterIncomeCategorySub


class TransactionExpense(TransactionBase):
    """
    Expense Transaction
    """
    expenseDate = models.DateField()
    amount = models.BigIntegerField()
    paymentRecipientName = models.CharField(max_length=30, blank=True, default='')
    note = models.TextField()
    masterExpenseCategorySub = models.ForeignKey(MasterExpenseCategorySub, on_delete=models.CASCADE)


class TransactionIncome(TransactionBase):
    """
    Income Transaction
    """
    incomeDate = models.DateField()
    amount = models.BigIntegerField()
    paymentSourceName = models.CharField(max_length=30, blank=True, default='')
    note = models.TextField()
    masterIncomeCategorySub = models.ForeignKey(MasterIncomeCategorySub, on_delete=models.CASCADE)

