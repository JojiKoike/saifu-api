from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from .base import viewbase
from ..models.master.expense import MExpenseCategoryMain
from ..models.transaction.expense import TExpense
from ..serializers.expense import ExpenseCategorySerializer, ExpenseSerializer


class ExpenseCategoryViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Expense Category List
    """
    queryset = MExpenseCategoryMain.objects.all()
    serializer_class = ExpenseCategorySerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = ExpenseCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Implement update, partial_update, destroy


class ExpenseViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Expense
    """
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return TExpense.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Implement update, partial_update, destroy
