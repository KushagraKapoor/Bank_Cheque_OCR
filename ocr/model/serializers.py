from rest_framework import serializers
from .models import CheckData

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckData
        fields = ['bank_name', 'check_image', 'ifsc_code', 'account_number', 'micr_details', 'name', 'amount', 'amount_in_dg', 'signature_present', 'cheque_id']
