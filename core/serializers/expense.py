from rest_framework import serializers
from ..models.master.expense import MExpenseCategoryMain, MExpenseCategorySub
from ..models.transaction.expense import TExpense, TExpenseDetail
from core.models.user.saifu import USaifu


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
        fields = ('id', 'name', 'm_expense_category_main')


class ExpenseCategorySerializer(serializers.ModelSerializer):
    """
    Expense Category (Main & Sub) Serializer
    """
    m_expense_category_subs = ExpenseCategorySubSerializer(many=True, read_only=True)

    class Meta:
        model = MExpenseCategoryMain
        fields = ('id', 'name', 'm_expense_category_subs')


class ExpenseDetailSerializer(serializers.ModelSerializer):
    """
    Expense Detail Serializer
    """
    u_saifu = serializers.UUIDField(required=True, write_only=True)

    class Meta:
        model = TExpenseDetail
        fields = ('id', 'amount', 'm_expense_category_sub', 'u_saifu', 'owner')


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Expense Serializer
    """
    t_expense_details = ExpenseDetailSerializer(many=True)

    class Meta:
        model = TExpense
        fields = ('id', 'payment_recipient_name', 'expense_date', 'note', 't_expense_details')

    def create(self, validated_data):
        """
        Record Expense
        :param validated_data: Expense, ExpenseDetails
        :return: Expense
        """
        expense_details_data = validated_data.pop('t_expense_details')
        expense = TExpense.objects.create(**validated_data)
        for expense_detail_data in expense_details_data:
            """
            Step 2-1 : Get Each Expense detail amount
            """
            expense_amount = expense_detail_data.pop('amount')

            """
            Step 2-2 : Update Saifu Current Balance
            """
            u_saifu = USaifu.objects.get(pk=expense_detail_data.pop('u_saifu'))
            u_saifu.currentBalance -= expense_amount
            u_saifu.save()

            """
            Step 2-3 : Create Expense Detail records
            """
            TExpenseDetail.objects.create(t_expense=expense, u_saifu=u_saifu,
                                          amount=expense_amount, **expense_detail_data)

        return expense
