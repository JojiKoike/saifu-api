from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from core.models.master.asset import MAssetCategoryMain
from core.models.user.asset import UAsset
from ..serializers.asset import AssetCategorySerializer, AssetSerializer
from .base import viewbase


class AssetCategoryViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Asset Category
    """
    queryset = MAssetCategoryMain.objects.all()
    serializer_class = AssetCategorySerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = AssetCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(data=serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Implement update, partial_update, destroy


class AssetViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Asset
    """
    serializer_class = AssetSerializer

    def get_queryset(self):
        return UAsset.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # TODO Implement update, partial_update, destroy
