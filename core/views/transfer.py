from rest_framework import generics
from ..models.transaction.transfer import TTransferBetweenSaifu
from ..serializers.transfer import TransferBetweenSaifuSerializer


class TransferBetweenSaifuList(generics.ListCreateAPIView):
    """
    Transfer Between Saifu List View
    """
    queryset = TTransferBetweenSaifu.objects.all()
    serializer_class = TransferBetweenSaifuSerializer
