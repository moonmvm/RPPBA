from django.contrib import admin

from utils.mixins import RelatedObjectLinkMixin
from . import models


class ClienteleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
    )


class WaybillAdmin(RelatedObjectLinkMixin, admin.ModelAdmin):
    link_fields = ['clientele_participant']
    list_display = (
        'clientele_participant',
        'date_of_sending',
        'first_check_passed',
        'second_check_passed',
    )


admin.site.register(models.Clientele, ClienteleAdmin)
admin.site.register(models.Waybill, WaybillAdmin)
