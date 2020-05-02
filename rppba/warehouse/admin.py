from django.contrib import admin

from utils.mixins import RelatedObjectLinkMixin
from . import models


class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
        'cells',
        'free_cells',
    )
    exclude = ['free_cells']

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        return True


class CellAdmin(RelatedObjectLinkMixin, admin.ModelAdmin):
    link_fields = ['warehouse']
    list_display = (
        'pk',
        'warehouse_link',
        'size',
        'actual_size',
    )

    exclude = ['actual_size']


admin.site.register(models.Warehouse, WarehouseAdmin)
admin.site.register(models.Cell, CellAdmin)
