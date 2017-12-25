from rest_framework import serializers
from ..models.master.income import MIncomeCategoryMain, MIncomeCategorySub
from ..models.master.saifu import MSaifu
from ..models.transaction.income import TIncome, TIncomeDetail


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


class IncomeSerializer(serializers.ModelSerializer):
    """
    Income Serializer
    """
    income_details = IncomeDetailSerializer(many=True)

    class Meta:
        model = TIncome
        fields = ('id', 'paymentSourceName', 'incomeDate', 'note', 'income_details')

    def create(self, validated_data):
        income_details_data = validated_data.pop('income_details')
        income = TIncome.objects.create(**validated_data)
        for income_detail_data in income_details_data:
            """
            Step.1 : 収入明細金額保存
            """
            income_amount = income_detail_data.pop('amount')
            """
            Step.2 : 収入先Saifuの残高更新
            """
            m_saifu = MSaifu.objects.get(pk=income_detail_data.pop('mSaifu'))
            m_saifu.currentBalance += income_amount
            m_saifu.save()
            """
            Step.3 : 収入明細レコードの生成
            """
            TIncomeDetail.objects.create(tIncome=income, mSaifu=m_saifu,
                                         amount=income_amount, **income_detail_data)
        return income


