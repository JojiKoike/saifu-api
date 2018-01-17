from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from .base import viewbase
from ..models.transaction.transfer import TTransferBetweenSaifu, \
    TTransferBetweenSaifuAndAsset, TTransferBetweenSaifuAndDebt
from ..serializers.transfer import TransferBetweenSaifuSerializer, \
    TransferBetweenSaifuAndAssetSerializer, TransferBetweenSaifuAndDebtSerializer


class TransferBetweenSaifuViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Transfer Between Saifu and the other Saifu
    """
    serializer_class = TransferBetweenSaifuSerializer

    def get_queryset(self):
        return TTransferBetweenSaifu.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = TransferBetweenSaifuSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(data=serializer.data)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Implement update, partial_update, destroy


class TransferBetweenSaifuAndAssetViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Transfer Between Saifu and Asset
    """
    serializer_class = TransferBetweenSaifuAndAssetSerializer

    def get_queryset(self):
        return TTransferBetweenSaifuAndAsset.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = TransferBetweenSaifuAndAssetSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(data=serializer.data)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Implement update, partial_update, destroy


class TransferBetweenSaifuAndDebtViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Transfer Between Saifu And Debt
    """
    serializer_class = TransferBetweenSaifuAndDebtSerializer

    def get_queryset(self):
        return TTransferBetweenSaifuAndDebt.objects.filter(owner=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = TransferBetweenSaifuAndDebtSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(data=serializer.data)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Implement update, partial_update, destroy
