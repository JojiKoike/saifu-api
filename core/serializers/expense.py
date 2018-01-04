from rest_framework import serializers
from django.db import transaction
from ..models.master.expense import MExpenseCategoryMain, MExpenseCategorySub
from ..models.transaction.expense import TExpense, TExpenseDetail
from core.models.user.saifu import USaifu


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
    m_expense_category_subs = ExpenseCategorySubSerializer(many=True)

    class Meta:
        model = MExpenseCategoryMain
        fields = ('id', 'name', 'm_expense_category_subs')

    @transaction.atomic
    def create(self, validated_data):
        m_expense_category_subs_data = validated_data.pop('m_expense_category_subs')
        m_expense_category_main = MExpenseCategoryMain.objects.create(**validated_data)
        for m_expense_category_sub_data in m_expense_category_subs_data:
            MExpenseCategorySub.objects.create(m_expense_category_main=m_expense_category_main,
                                               **m_expense_category_sub_data)
        return m_expense_category_main


class ExpenseDetailSerializer(serializers.ModelSerializer):
    """
    Expense Detail Serializer
    """
    u_saifu = serializers.UUIDField(required=True)

    class Meta:
        model = TExpenseDetail
        fields = ('id', 'amount', 'm_expense_category_sub', 'u_saifu')


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Expense Serializer
    """
    t_expense_details = ExpenseDetailSerializer(many=True)

    class Meta:
        model = TExpense
        fields = ('id', 'payment_recipient_name', 'expense_date', 'note', 't_expense_details')

    @transaction.atomic
    def create(self, validated_data):
        """
        Record Expense
        :param validated_data: Expense, ExpenseDetails
        :return: Expense
        """

        """
        Step 1 : Create Parent Expense Record
        """
        expense_details_data = validated_data.pop('t_expense_details')
        expense = TExpense.objects.create(**validated_data)

        """
        Step 2 : Get Owner Data
        """
        owner = validated_data.pop('owner')

        """
        Step 3 : Create Owner's Saifu List
        """
        u_saifu_query_set = USaifu.objects.filter(owner=owner)

        """
        Step 4 : Record Each Expense Detail 
        """
        for expense_detail_data in expense_details_data:
            """
            Step 2-1 : Get Each Expense detail amount
            """
            expense_amount = expense_detail_data.pop('amount')

            """
            Step 2-2 : Update Saifu Current Balance
            """
            u_saifu = u_saifu_query_set.get(pk=expense_detail_data.pop('u_saifu'))
            u_saifu.current_balance -= expense_amount
            u_saifu.save()

            """
            Step 2-3 : Create Expense Detail records
            """
            TExpenseDetail.objects.create(t_expense=expense, u_saifu=u_saifu,
                                          amount=expense_amount, owner=owner, **expense_detail_data)

        return expense
