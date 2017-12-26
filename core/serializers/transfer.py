from rest_framework import serializers
from ..models.transaction.transfer import TTransferBetweenSaifu
from ..models.master.saifu import MSaifu


class TransferBetweenSaifuSerializer(serializers.ModelSerializer):
    fromSaifu = serializers.UUIDField(required=True, write_only=True)
    toSaifu = serializers.UUIDField(required=True, write_only=True)
    """
    Transfer Between Saifu Serializer
    """
    class Meta:
        model = TTransferBetweenSaifu
        fields = ('id', 'transferDate', 'amount', 'note', 'fromSaifu', 'toSaifu')

    def create(self, validated_data):
        """
        Create Transfer Between Saifu Record
        :param validated_data:
        :return: TransferBetweenSaifu
        """

        """
        Step 1 : Get Transfer Amount
        """
        transfer_amount = validated_data.pop('amount')
        """
        Step 2 : Update From Saifu Current Balance
        """
        from_saifu = MSaifu.objects.get(pk=validated_data.pop('fromSaifu'))
        from_saifu.currentBalance -= transfer_amount
        from_saifu.save()
        """
        Step 3 : Update To Saifu Current Balance
        """
        to_saifu = MSaifu.objects.get(pk=validated_data.pop('toSaifu'))
        to_saifu.currentBalance += transfer_amount
        to_saifu.save()
        """
        Step 4 : Create Transfer Between Saifu Transaction Record
        """
        transfer_between_saifu = TTransferBetweenSaifu.objects.create(amount=transfer_amount, fromSaifu=from_saifu,
                                                                      toSaifu=to_saifu, **validated_data)

        return transfer_between_saifu
