from rest_framework import serializers
from django.db import transaction
from ..models.master.income import MIncomeCategoryMain, MIncomeCategorySub
from core.models.user.saifu import USaifu
from ..models.transaction.income import TIncome, TIncomeDetail
from ..models.transaction.credit import TCredit
from ..serializers.credit import CreditSerializer


class IncomeCategorySubSerializer(serializers.ModelSerializer):
    """
    Income Category Sub Serializer
    """
    class Meta:
        model = MIncomeCategorySub
        fields = ('id', 'name', 'm_income_category_main')


class IncomeCategorySerializer(serializers.ModelSerializer):
    """
    Income Category Serializer (Main and Sub)
    """
    m_income_category_subs = IncomeCategorySubSerializer(many=True)

    class Meta:
        model = MIncomeCategoryMain
        fields = ('id', 'name', "m_income_category_subs")

    @transaction.atomic
    def create(self, validated_data):
        income_category_subs_data = validated_data.pop('m_income_category_subs')
        m_income_category_main = MIncomeCategoryMain.objects.craete(**validated_data)
        for income_category_sub_data in income_category_subs_data:
            MIncomeCategorySub.objects.create(m_income_category_main=m_income_category_main,
                                              **income_category_sub_data)
        return m_income_category_main


class IncomeDetailSerializer(serializers.ModelSerializer):
    """
    Income Detail Serializer
    """
    u_saifu = serializers.UUIDField(required=True)

    class Meta:
        model = TIncomeDetail
        fields = ('id', 'amount', 'm_income_category_sub', 'u_saifu')


class IncomeSerializer(serializers.ModelSerializer):
    """
    Income Serializer
    """
    t_income_details = IncomeDetailSerializer(many=True)
    t_credits = CreditSerializer(many=True)

    class Meta:
        model = TIncome
        fields = ('id', 'payment_source_name', 'income_date', 'note', 't_income_details', 't_credits')

    @transaction.atomic
    def create(self, validated_data):
        """
        Create Income Record
        :param validated_data: Income, IncomeDetails, Credits
        :return: Income
        """

        """
        Step 1 : Create Parent Income Record
        """
        income_details_data = validated_data.pop('t_income_details')
        credits_data = validated_data.pop('t_credits')
        income = TIncome.objects.create(**validated_data)

        """
        Step 2 : Get Owner Data
        """
        owner = validated_data.pop('owner')

        """
        Step 3 : Create Owner's Saifu List
        """
        u_saifu_query_set = USaifu.objects.filter(owner=owner)

        """
        Step 4 : Record Each Expense detail and Credit
        """
        for income_detail_data in income_details_data:
            """
            Step.2-1 : Get each Income Detail amount
            """
            income_amount = income_detail_data.pop('amount')
            """
            Step.2-2 : Update Saifu current balance
            """
            u_saifu = u_saifu_query_set.get(pk=income_detail_data.pop('m_saifu'))
            u_saifu.currentBalance += income_amount
            u_saifu.save()
            """
            Step.2-3 : Create Income Detail records
            """
            TIncomeDetail.objects.create(t_income=income, m_saifu=u_saifu,
                                         amount=income_amount, owner=owner, **income_detail_data)

        """
        Step 5 : Create Credit records
        """
        for credit_data in credits_data:
            TCredit.objects.create(tIncome=income, owner=owner, **credit_data)

        return income


