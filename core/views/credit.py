from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from .base import viewbase
from ..models.master.credit import MCreditCategoryMain
from ..models.transaction.credit import TCredit
from ..serializers.credit import CreditCategorySerializer, CreditSerializer


class CreditCategoryViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Credit Category List
    """
    queryset = MCreditCategoryMain.objects.all()
    serializer_class = CreditCategorySerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = CreditCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Implement update, partial_update, destroy


class CreditViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Credit Transaction
    """
    serializer_class = CreditSerializer

    def get_queryset(self):
        return TCredit.objects.filter(owner=self.request.user)

    # TODO Implement update, partial_update, destroy
