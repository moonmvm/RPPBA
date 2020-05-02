from django.db import models

from utils import constants, factories_utils


class Clientele(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    clientele_type = models.CharField(max_length=10, choices=constants.CLIENTELE_TYPE)

    def __str__(self):
        return '{}. Type: {}'.format(self.name, self.clientele_type)


class Waybill(models.Model):
    number = models.CharField(max_length=20, default=factories_utils.generate_barcode(),
                              blank=False, null=False)
    firm_participant = models.ForeignKey(Clientele, on_delete=models.CASCADE,
                                         related_name='firm_participant_waybill')
    clientele_participant = models.ForeignKey(Clientele, on_delete=models.CASCADE,
                                              related_name='clientele_participant_waybill')
    products = models.ManyToManyField('products.Product', related_name='product_waybill')
    date_of_sending = models.DateTimeField(auto_now_add=True)
    first_check_passed = models.BooleanField(default=False)
    second_check_passed = models.BooleanField(default=False)
    waybill_type = models.CharField(max_length=15, choices=constants.WAYBILL_TYPE,
                                    default=constants.Waybill.SUPPLY.value)

    def __str__(self):
        return 'Number: {}. Date of sending: {}'.format(self.pk, self.date_of_sending)
