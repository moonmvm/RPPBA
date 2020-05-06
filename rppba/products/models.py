from django.db import models

from utils import constants


class Nomenclature(models.Model):
    name = models.CharField(max_length=40)
    nomenclature_type = models.CharField(max_length=15, choices=constants.NOMENCLATURE_TYPE)
    kind_of_nomenclature = models.CharField(max_length=20, choices=constants.NOMENCLATURE_KIND)

    def __str__(self):
        return 'Name: {}. Type: {}. Kind: {}'.format(self.name, self.nomenclature_type, self.kind_of_nomenclature)


class Product(models.Model):
    cell = models.ManyToManyField('warehouse.Cell', related_name='product', blank=True)
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.PROTECT, related_name='product')
    image = models.ImageField(blank=True, null=True)
    amount = models.PositiveIntegerField()
    price = models.FloatField()
    date_of_manufacture = models.DateTimeField()
    receiving_date = models.DateTimeField()

    def __str__(self):
        return 'Product id: {}. Nomenclature: {}'.format(self.pk, self.nomenclature)
