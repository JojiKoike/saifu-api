from rest_framework import serializers
from ..models.master.income import MIncomeCategoryMain, MIncomeCategorySub
from core.models.user.saifu import USaifu
from ..models.transaction.income import TIncome, TIncomeDetail
from ..models.transaction.credit import TCredit
from ..serializers.credit import CreditSerializer


class IncomeCategoryMainSerializer(serializers.ModelSerializer):
    """
    Income Category Sub Serializer
    """
    class Meta:
        model = MIncomeCategoryMain
        fields = ('id', 'name')


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
    m_income_category_subs = IncomeCategorySubSerializer(many=True, read_only=True)

    class Meta:
        model = MIncomeCategoryMain
        fields = ('id', 'name', "m_income_category_subs")


class IncomeDetailSerializer(serializers.ModelSerializer):
    """
    Income Detail Serializer
    """
    u_saifu = serializers.UUIDField(required=True, write_only=True)

    class Meta:
        model = TIncomeDetail
        fields = ('id', 'amount', 'm_income_category_sub', 'u_saifu', 'owner')


class IncomeSerializer(serializers.ModelSerializer):
    """
    Income Serializer
    """
    t_income_details = IncomeDetailSerializer(many=True)
    credits = CreditSerializer(many=True)

    class Meta:
        model = TIncome
        fields = ('id', 'payment_source_name', 'income_date', 'note', 't_income_details', 't_credits', 'owner')

    def create(self, validated_data):
        """
        Create Income Record
        :param validated_data: Income, IncomeDetails, Credits
        :return: Income
        """

        """
        Step.1 : Get Income Details and Credits data from Input JSON.
        (Attention : These procedure must be done before Income record create
                      because these attributes aren't included in TIncome.)
        """
        income_details_data = validated_data.pop('t_income_details')
        credits_data = validated_data.pop('t_credits')

        """
        Step.2 : Create Income Parent Object
        """
        income = TIncome.objects.create(**validated_data)
        for income_detail_data in income_details_data:
            """
            Step.2-1 : Get each Income Detail amount
            """
            income_amount = income_detail_data.pop('amount')
            """
            Step.2-2 : Update Saifu current balance
            """
            u_saifu = USaifu.objects.get(pk=income_detail_data.pop('m_saifu'))
            u_saifu.currentBalance += income_amount
            u_saifu.save()
            """
            Step.2-3 : Create Income Detail records
            """
            TIncomeDetail.objects.create(t_income=income, m_saifu=u_saifu,
                                         amount=income_amount, **income_detail_data)

        """
        Step.3 : Create Credit records
        """
        for credit_data in credits_data:
            TCredit.objects.create(tIncome=income, **credit_data)

        return income


