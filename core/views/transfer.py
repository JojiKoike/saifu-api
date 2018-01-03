from rest_framework import generics
from .base import viewbase
from ..models.transaction.transfer import TTransferBetweenSaifu
from ..serializers.transfer import TransferBetweenSaifuSerializer


class TransferBetweenSaifuList(generics.ListCreateAPIView):
    """
    Transfer Between Saifu List View
    """
    queryset = TTransferBetweenSaifu.objects.all()
    serializer_class = TransferBetweenSaifuSerializer


class TransferBetweenSaifuViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Transfer Between Saifu
    """
    serializer_class = TransferBetweenSaifuSerializer

    def get_queryset(self):
        return TTransferBetweenSaifu.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
