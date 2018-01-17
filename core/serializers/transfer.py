from rest_framework import serializers
from ..models.transaction.transfer import TTransferBetweenSaifu, \
    TTransferBetweenSaifuAndAsset, TTransferBetweenSaifuAndDebt
from ..models.transaction.asset import TAssetEvaluate
from ..models.transaction.debt import TDebtGain
from core.models.user.saifu import USaifu
from core.models.user.asset import UAsset
from core.models.user.debt import UDebt


class TransferBetweenSaifuSerializer(serializers.ModelSerializer):
    """
    Transfer Between Saifu Serializer
    """
    from_u_saifu = serializers.UUIDField(required=True)
    to_u_saifu = serializers.UUIDField(required=True)

    class Meta:
        model = TTransferBetweenSaifu
        fields = ('id', 'transfer_date', 'amount', 'note', 'from_u_saifu', 'to_u_saifu')

    def create(self, validated_data):
        """
        Create Transfer Between Saifu Record
        :param validated_data:
        :return: TransferBetweenSaifu
        """

        transfer_amount = validated_data.pop('amount')
        owner = validated_data.pop('owner')
        u_saifu_query_set = USaifu.objects.filter(owner=owner)

        """
        Update From Saifu Current Balance
        """
        from_u_saifu = u_saifu_query_set.get(pk=validated_data.pop('from_u_saifu'))
        # TODO Validate transfer_amount <= current_balance
        from_u_saifu.current_balance -= transfer_amount
        from_u_saifu.save()

        """
        Update To Saifu Current Balance
        """
        to_u_saifu = u_saifu_query_set.get(pk=validated_data.pop('to_u_saifu'))
        to_u_saifu.current_balance += transfer_amount
        to_u_saifu.save()

        """
        Create Transfer Between Saifu Transaction Record
        """
        transfer_between_saifu = TTransferBetweenSaifu.objects.create(amount=transfer_amount,
                                                                      from_u_saifu=from_u_saifu,
                                                                      to_u_saifu=to_u_saifu, owner=owner,
                                                                      **validated_data)

        return transfer_between_saifu


class TransferBetweenSaifuAndAssetSerializer(serializers.ModelSerializer):
    """
    Transfer Between Saifu And Asset Serializer
    """
    u_saifu = serializers.UUIDField(required=True)
    u_asset = serializers.UUIDField(required=True)

    class Meta:
        model = TTransferBetweenSaifuAndAsset
        fields = ('id', 'transfer_date', 'amount', 'note', 'u_saifu', 'u_asset')

    def create(self, validated_data):
        """
        Create Transfer Between Saifu and Asset Record
        :param validated_data:
        :return: TTransferBetweenSaifuAndAsset
        """
        transfer_date = validated_data.pop('transfer_date')
        transfer_amount = validated_data.pop('amount')
        note = validated_data.pop('note')
        owner = validated_data.pop('owner')
        u_saifu_query_set = USaifu.objects.filter(owner=owner)
        u_asset_query_set = UAsset.objects.filter(owner=owner)

        """
        Update Saifu Current Balance
        """
        u_saifu = u_saifu_query_set.get(pk=validated_data.pop('u_saifu'))
        u_saifu.current_balance -= transfer_amount
        # TODO Validate transfer_amount <= current_evaluated_amount
        u_saifu.save()

        """
        Update Asset Current Capital Amount and Current Evaluated Amount
        """
        u_asset = u_asset_query_set.get(pk=validated_data.pop('u_asset'))
        u_asset.current_capital_amount += (transfer_amount if transfer_amount > 0 else 0)
        u_asset.current_evaluated_amount += transfer_amount
        u_asset.save()

        """
        Create Asset Evaluate Transaction Record
        """
        TAssetEvaluate.objects.create(
            evaluate_date=transfer_date,
            evaluated_amount=u_asset.current_evaluated_amount,
            note=note,
            u_asset=u_asset,
            owner=owner)

        """
        Create Transfer Between Saifu And Asset Record
        """
        transfer_between_saifu_and_asset = TTransferBetweenSaifuAndAsset.objects.create(
            transfer_date=transfer_date,
            amount=transfer_amount,
            note=note,
            u_saifu=u_saifu, u_asset=u_asset,
            owner=owner)

        return transfer_between_saifu_and_asset


class TransferBetweenSaifuAndDebtSerializer(serializers.ModelSerializer):
    """
    Transfer Between Saifu And Asset Serializer
    """
    u_saifu = serializers.UUIDField(required=True)
    u_debt = serializers.UUIDField(required=True)

    class Meta:
        model = TTransferBetweenSaifuAndDebt
        fields = ('id', 'transfer_date', 'amount', 'note', 'u_saifu', 'u_debt')

    def create(self, validated_data):
        """
        Create Transfer Between Saifu and Asset Record
        :param validated_data:
        :return: TTransferBetweenSaifuAndAsset
        """
        transfer_date = validated_data.pop('transfer_date')
        transfer_amount = validated_data.pop('amount')
        note = validated_data.pop('note')
        owner = validated_data.pop('owner')
        u_saifu_query_set = USaifu.objects.filter(owner=owner)
        u_debt_query_set = UDebt.objects.filter(owner=owner)

        """
        Update Saifu Current Balance
        """
        u_saifu = u_saifu_query_set.get(pk=validated_data.pop('u_saifu'))
        u_saifu.current_balance -= transfer_amount
        # TODO Validate transfer_amount <= current_evaluated_amount
        u_saifu.save()

        """
        Update Debt Current Principal Amount and Current Gained Amount
        """
        u_debt = u_debt_query_set.get(pk=validated_data.pop('u_debt'))
        u_debt.current_principal_amount -= (transfer_amount if transfer_amount < 0 else 0)
        u_debt.current_gained_amount -= transfer_amount
        u_debt.save()

        """
        Create Asset Evaluate Transaction Record
        """
        TDebtGain.objects.create(
            gained_date=transfer_date,
            gained_amount=u_debt.current_gained_amount,
            note=note,
            u_debt=u_debt,
            owner=owner)

        """
        Create Transfer Between Saifu And Asset Record
        """
        transfer_between_saifu_and_debt = TTransferBetweenSaifuAndDebt.objects.create(
            transfer_date=transfer_date,
            amount=transfer_amount,
            note=note,
            u_saifu=u_saifu, u_debt=u_debt,
            owner=owner)

        return transfer_between_saifu_and_debt
