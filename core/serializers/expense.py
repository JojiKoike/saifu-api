from rest_framework import serializers
from ..models.master.expense import MExpenseCategoryMain, MExpenseCategorySub
from ..models.transaction.expense import TExpense, TExpenseDetail


class ExpenseCategoryMainSerializer(serializers.ModelSerializer):
    """
    Expense Category Main Serializer
    """
    class Meta:
        model = MExpenseCategoryMain
        fields = ('id', 'name')


class ExpenseCategorySubSerializer(serializers.ModelSerializer):
    """
    Expense Category Sub Serializer
    """
    class Meta:
        model = MExpenseCategorySub
        fields = ('id', 'name', 'mExpenseCategoryMain')


class ExpenseCategorySerializer(serializers.ModelSerializer):
    """
    Expense Category Serializer
    """
    expense_category_subs = ExpenseCategorySubSerializer(many=True)

    class Meta:
        model = MExpenseCategoryMain
        fields = ('id', 'name', 'expense_category_subs')
