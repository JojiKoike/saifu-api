from rest_framework import serializers
from ..models.master.income import MIncomeCategoryMain, MIncomeCategorySub
from ..models.master.saifu import MSaifu
from ..models.transaction.income import TIncome, TIncomeDetail
from ..models.transaction.saifu import TSaifuHistory


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
    Income Detail Transaction Serializer
    """
    class Meta:
        model = TIncomeDetail
        fields = ('id', 'amount', 'tIncome', 'mIncomeCategorySub', 'tSaifuHistory')


class Income(object):
    """
    Income Object
    """
    def __init__(self, paymentSourceName, incomeDate, note, incomeDetails):
        self.paymentSourceName = paymentSourceName
        self.incomeDate = incomeDate
        self.note = note
        self.incomeDetails = incomeDetails


class IncomeDetailInput(object):
    """
    Income Detail Input Object
    """
    def __init__(self, amount, id_income_category_sub, id_saifu):
        self.amount = amount
        self.id_income_category_sub = id_income_category_sub
        self.id_saifu = id_saifu


class IncomeDetailInputsSerializer(serializers.Serializer):
    """
    Income Detail Input Serializer
    """
    amount = serializers.IntegerField()
    id_income_category_sub = serializers.UUIDField()
    id_saifu = serializers.UUIDField()

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.id_income_category_sub = \
            validated_data.get('id_income_category_sub', instance.id_income_category_sub)
        instance.id_saifu = validated_data.get('id_saifu', instance.id_saifu)
        return instance

    def create(self, validated_data):
        return IncomeDetailInput(**validated_data)


class IncomeEditSerializer(serializers.Serializer):

    paymentSourceName = serializers.CharField(max_length=30)
    incomeDate = serializers.DateField()
    note = serializers.CharField()
    incomeDetails = IncomeDetailInputsSerializer(many=True)

    """
    Income update & create Serializer
    """
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        """
        収入記録処理の流れ
        １．親帳票オブジェクト保存
        ２．各明細に、収入金額、収入サブカテゴリのUUID, 収入先SaifuのUUID
        :param validated_data:
        :return: Response
        """
        income_details_data = validated_data.pop('incomeDetails')
        print(income_details_data)
        income = TIncome.objects.create(**validated_data)
        for income_detail_data in income_details_data:
            """
            Step1 : Update Saifu CurrentBalance
            """
            saifu = MSaifu.objects.get(pk=income_detail_data.pop('id_saifu'))
            amount = income_detail_data.pop('amount')
            saifu.currentBalance += amount
            saifu.save()
            """
            Step2 : Create Saifu History Record
            """
            saifu_history = TSaifuHistory.objects.create(
                recordDate=validated_data.pop('incomeDate'),
                balance=saifu.currentBalance,
                mSaifu=saifu)
            """
            Step3 : Create Income Detail Record
            """
            TIncomeDetail.objects.create(tIncome=income,
                                         amount=amount,
                                         mIncomeCategorySub=
                                         MIncomeCategorySub.objects
                                         .get(pk=income_detail_data.pop('id_income_category_sub')),
                                         tSaifuHistory=saifu_history)

        return income
