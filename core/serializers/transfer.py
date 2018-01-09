from rest_framework import serializers
from ..models.transaction.transfer import TTransferBetweenSaifu, TTransferBetweenSaifuAndAsset
from ..models.transaction.asset import TAssetEvaluate
from core.models.user.saifu import USaifu
from core.models.user.asset import UAsset


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
        u_saifu -= transfer_amount
        u_saifu.save()

        """
        Update Asset Current Capital Amount and Current Evaluated Amount
        """
        u_asset = u_asset_query_set.get(pk=validated_data.pop('u_asset'))
        u_asset.current_capital_amount += transfer_amount
        if u_asset.current_capital_amount < 0:
            u_asset.current_capital_amount = 0
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


