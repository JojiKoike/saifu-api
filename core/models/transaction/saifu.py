from django.db import models

from ..base.transactionbase import TransactionBase
from ..master.saifu import MSaifu


class TSaifuHistory(TransactionBase):
    """
    Saifu History Transaction Model
    """
    recordDate = models.DateField()
    balance = models.BigIntegerField()
    msaifu = models.ForeignKey(MSaifu, on_delete=models.CASCADE)