from django.db import models

class CheckData(models.Model):
    bank_choices = [
        ('general', 'General Bank'),  # Added 'General Bank' option
        ('canara', 'Canara Bank'),
        ('syndicate', 'Syndicate Bank'),
        ('icici', 'ICICI Bank'),
        ('axis', 'Axis Bank'),
    ]
    bank_name = models.CharField(max_length=50, choices=bank_choices)
    check_image = models.ImageField(upload_to='check_images/')
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    micr_details = models.JSONField(blank=True, null=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    amount = models.CharField(max_length=40, blank=True, null=True)
    amount_in_dg = models.CharField(max_length=40, blank=True, null=True)
    signature_present = models.BooleanField(default=False)

    def __str__(self):
        return f"CheckData {self.id} - {self.bank_name}"
