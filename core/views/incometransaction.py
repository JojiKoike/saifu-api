from core.serializers.income import IncomeSerializer
from core.models.transaction.income import TIncome

from rest_framework import generics


class Income(generics.ListCreateAPIView):
    queryset = TIncome.objects.all()
    serializer_class = IncomeSerializer
