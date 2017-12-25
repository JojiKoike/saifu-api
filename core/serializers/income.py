from rest_framework import serializers
from ..models.master.income import MIncomeCategoryMain, MIncomeCategorySub
from ..models.master.saifu import MSaifu
from ..models.transaction.income import TIncome, TIncomeDetail
from ..models.transaction.credit import TCredit


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
        fields = ('id', 'name', 'mIncomeCategoryMain')


class IncomeCategorySerializer(serializers.ModelSerializer):
    """
    Income Category Serializer (Main and Sub)
    """
    income_category_sub = IncomeCategorySubSerializer(many=True, read_only=True)

    class Meta:
        model = MIncomeCategoryMain
        fields = ('id', 'name', "income_category_sub")


class IncomeDetailSerializer(serializers.ModelSerializer):
    """
    Income Detail Serializer
    """
    mSaifu = serializers.UUIDField(required=True, write_only=True)

    class Meta:
        model = TIncomeDetail
        fields = ('id', 'amount', 'mIncomeCategorySub', 'mSaifu')


class CreditSerializer(serializers.ModelSerializer):
    """
    Credit Serializer
    """
    class Meta:
        model = TCredit
        fields = ('id', 'amount', 'mCreditCategorySub')


class IncomeSerializer(serializers.ModelSerializer):
    """
    Income Serializer
    """
    income_details = IncomeDetailSerializer(many=True)
    credits = CreditSerializer(many=True)

    class Meta:
        model = TIncome
        fields = ('id', 'paymentSourceName', 'incomeDate', 'note', 'income_details', 'credits')

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
        income_details_data = validated_data.pop('income_details')
        credits_data = validated_data.pop('credits')

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
            m_saifu = MSaifu.objects.get(pk=income_detail_data.pop('mSaifu'))
            m_saifu.currentBalance += income_amount
            m_saifu.save()
            """
            Step.2-3 : Create Income Detail records
            """
            TIncomeDetail.objects.create(tIncome=income, mSaifu=m_saifu,
                                         amount=income_amount, **income_detail_data)

        """
        Step.3 : Create Credit records
        """
        for credit_data in credits_data:
            TCredit.objects.create(tIncome=income, **credit_data)

        return income


