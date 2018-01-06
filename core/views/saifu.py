from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from core.models.master.saifu import MSaifuCategoryMain
from core.models.user.saifu import USaifu
from .base import viewbase
from ..serializers.saifu import SaifuCategorySerializer, SaifuSerializer


class SaifuCategoryViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Saifu Category
    """
    queryset = MSaifuCategoryMain.objects.all()
    serializer_class = SaifuCategorySerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = SaifuCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaifuViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Saifu
    """
    serializer_class = SaifuSerializer

    def get_queryset(self):
        return USaifu.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
