from rest_framework import serializers
from ..models.master.expense import MExpenseCategoryMain, MExpenseCategorySub
from ..models.transaction.expense import TExpense, TExpenseDetail
from ..models.master.saifu import MSaifu


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


class ExpenseDetailSerializer(serializers.ModelSerializer):
    """
    Expense Detail Serializer
    """
    mSaifu = serializers.UUIDField(required=True, write_only=True)

    class Meta:
        model = TExpenseDetail
        fields = ('id', 'amount', 'mExpenseCategorySub', 'mSaifu')


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Expense Serializer
    """
    expense_details = ExpenseDetailSerializer(many=True)

    class Meta:
        model = TExpense
        fields = ('id', 'paymentRecipientName', 'expenseDate', 'note', 'expense_details')

    def create(self, validated_data):
        """
        Record Expense
        :param validated_data: Expense, ExpenseDetails
        :return: Expense
        """
        expense_details_data = validated_data.pop('expense_details')
        expense = TExpense.objects.create(**validated_data)
        for expense_detail_data in expense_details_data:
            """
            Step 2-1 : Get Each Expense detail amount
            """
            expense_amount = expense_detail_data.pop('amount')

            """
            Step 2-2 : Update Saifu Current Balance
            """
            m_saifu = MSaifu.objects.get(pk=expense_detail_data.pop('mSaifu'))
            m_saifu.currentBalance -= expense_amount
            m_saifu.save()

            """
            Step 2-3 : Create Expense Detail records
            """
            TExpenseDetail.objects.create(tExpense=expense, mSaifu=m_saifu,
                                          amount=expense_amount, **expense_detail_data)

        return expense
