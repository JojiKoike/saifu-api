from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from .base import viewbase
from ..models.transaction.transfer import TTransferBetweenSaifu
from ..serializers.transfer import TransferBetweenSaifuSerializer


class TransferBetweenSaifuViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Transfer Between Saifu
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

