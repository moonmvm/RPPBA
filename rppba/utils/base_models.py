from django.core.cache import cache
from django.db import models


class SingletonModel(models.Model):

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        cached = cache.get(cls.__name__)
        if cached is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
            cached = cache.get(cls.__name__)
        return cached
