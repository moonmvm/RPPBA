from django.contrib import admin

from . import models


class NomenclatureAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'nomenclature_type',
        'kind_of_nomenclature',
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'nomenclature',
        'amount',
        'price',
        'date_of_manufacture',
        'receiving_date',
    )


admin.site.register(models.Nomenclature, NomenclatureAdmin)
admin.site.register(models.Product, ProductAdmin)
