from rest_framework import serializers
from ..models.transaction.transfer import TTransferBetweenSaifu
from core.models.user.saifu import USaifu


class TransferBetweenSaifuSerializer(serializers.ModelSerializer):
    from_u_saifu = serializers.UUIDField(required=True, write_only=True)
    to_u_saifu = serializers.UUIDField(required=True, write_only=True)
    """
    Transfer Between Saifu Serializer
    """
    class Meta:
        model = TTransferBetweenSaifu
        fields = ('id', 'transfer_date', 'amount', 'note', 'from_u_saifu', 'to_u_saifu', 'owner')

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
        from_u_saifu = USaifu.objects.get(pk=validated_data.pop('from_u_saifu'))
        from_u_saifu.currentBalance -= transfer_amount
        from_u_saifu.save()
        """
        Step 3 : Update To Saifu Current Balance
        """
        to_u_saifu = USaifu.objects.get(pk=validated_data.pop('to_u_saifu'))
        to_u_saifu.currentBalance += transfer_amount
        to_u_saifu.save()
        """
        Step 4 : Create Transfer Between Saifu Transaction Record
        """
        transfer_between_saifu = TTransferBetweenSaifu.objects.create(amount=transfer_amount,
                                                                      from_u_saifu=from_u_saifu,
                                                                      to_u_saifu=to_u_saifu, **validated_data)

        return transfer_between_saifu
