import uuid
from django.db import models


class TransactionBase(models.Model):
    """
    Transaction Base Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True


class UnModifiableTransactionBase(models.Model):
    """
    Unmodifiable Transaction Base Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        abstract = True

