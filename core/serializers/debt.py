from rest_framework import serializers
from ..models.master.debt import MDebtCategoryMain, MDebtCategorySub
from ..models.user.debt import UDebt
from ..models.transaction.debt import TDebtGain


class DebtCategorySubSerializer(serializers.ModelSerializer):
    """
    Debt Sub Category Serializer
    """
    m_debt_category_main = serializers.UUIDField(read_only=True)

    class Meta:
        model = MDebtCategorySub
        fields = ('id', 'name', 'm_debt_category_main')


class DebtCategorySerializer(serializers.ModelSerializer):
    """
    Debt Category Serializer
    """
    m_debt_category_subs = DebtCategorySubSerializer(many=True)

    class Meta:
        model = MDebtCategoryMain
        fields = ('id', 'name', 'm_debt_category_subs')

    def create(self, validated_data):
        m_debt_category_subs_data = validated_data.pop('m_debt_category_subs')
        m_debt_category_main = MDebtCategoryMain.objects.create(**validated_data)
        for m_debt_category_sub_data in m_debt_category_subs_data:
            MDebtCategorySub.objects.create(
                m_debt_category_main=m_debt_category_main, **m_debt_category_sub_data)
        return m_debt_category_main


class DebtSerializer(serializers.ModelSerializer):
    """
    Debt Serializer
    """
    class Meta:
        model = UDebt
        fields = ('id', 'name', 'current_principal_amount',
                  'current_gained_amount', 'm_debt_category_sub')


class DebtGainSerializer(serializers.ModelSerializer):
    """
    Debt Gain Serializer
    """
    u_debt = serializers.UUIDField()

    class Meta:
        model = TDebtGain
        fields = ('id', 'gained_date', 'gained_amount', 'note', 'u_debt')

    def create(self, validated_data):
        """
        Create Debt Gain Record
        :param validated_data:
        :return:
        """
        gained_amount = validated_data.pop('gained_amount')
        owner = validated_data.pop('owner')

        """
        Update Current Gained Amount
        """
        u_debt_query_set = UDebt.objects.filter(owner=owner)
        u_debt = u_debt_query_set.get(pk=validated_data.pop('u_debt'))
        u_debt.current_gained_amount = gained_amount
        u_debt.save()

        """
        Create Debt Gain Record
        """
        t_debt_gain = TDebtGain.objects.create(
            gained_amount=gained_amount, u_debt=u_debt,
            owner=owner, **validated_data)

        return t_debt_gain
