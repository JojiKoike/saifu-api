from django.db import models
from ..base.transactionbase import UnModifiableTransactionBase
from ..master.saifu import MSaifu


class TTransferBetweenSaifu(UnModifiableTransactionBase):
    """
    Transfer Between Saifu Model
    """
    transferDate = models.DateField()
    amount = models.BigIntegerField()
    note = models.TextField()
    fromSaifu = models.ForeignKey(MSaifu, on_delete=models.CASCADE, related_name="from_saifu")
    toSaifu = models.ForeignKey(MSaifu, on_delete=models.CASCADE, related_name="to_saifu")
