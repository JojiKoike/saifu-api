from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from .base import viewbase
from ..models.master.income import MIncomeCategoryMain
from ..models.transaction.income import TIncome
from ..serializers.income import IncomeCategorySerializer, IncomeSerializer


class IncomeCategoryViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Income Category List
    """
    queryset = MIncomeCategoryMain.objects.all()
    serializer_class = IncomeCategorySerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = IncomeCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Implement update, partial_update, destroy


class IncomeViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Income
    """
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return TIncome.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Implement update, partial_update, destroy
