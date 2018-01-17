from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from core.models.master.debt import MDebtCategoryMain
from core.models.user.debt import UDebt
from core.models.transaction.debt import TDebtGain
from ..serializers.debt import DebtCategorySerializer, DebtSerializer, DebtGainSerializer
from .base import viewbase


class DebtCategoryViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Debt Category
    """
    queryset = MDebtCategoryMain.objects.all()
    serializer_class = DebtCategorySerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = DebtCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(data=serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Implement update, partial_update, destroy


class DebtViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Debt
    """
    serializer_class = DebtSerializer

    def get_queryset(self):
        return UDebt.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # TODO Implement update, partial_update, destroy


class DebtGainViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Debt Gain Transaction
    """
    serializer_class = DebtGainSerializer

    def get_queryset(self):
        return TDebtGain.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = DebtGainSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Implement update, partial_update, destroy
