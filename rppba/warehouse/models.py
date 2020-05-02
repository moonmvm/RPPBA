from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from utils.base_models import SingletonModel


class Warehouse(SingletonModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=150, null=False, blank=False)
    cells = models.PositiveIntegerField(default=0)
    free_cells = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Name: {}. Free cells: {}'.format(self.name, self.free_cells)


class Cell(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    size = models.PositiveIntegerField(default=0)
    actual_size = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Cell number: {}. Size: {}. Actual size: {}'.format(self.pk, self.size, self.actual_size)


@receiver(signals.pre_save, sender=Warehouse)
def set_free_cells(sender, instance=None, **kwargs):
    if sender.objects.count() == 0:
        instance.free_cells = instance.cells


@receiver(signals.post_save, sender=Cell)
def reduce_free_cells(sender, instance=None, created=False, **kwargs):
    if created:
        warehouse = Warehouse.load()
        warehouse.free_cells -= 1
        warehouse.save()


@receiver(signals.post_delete, sender=Cell)
def increase_free_cells(sender, instance=None, **kwargs):
    warehouse = Warehouse.load()
    warehouse.free_cells += 1
    warehouse.save()
