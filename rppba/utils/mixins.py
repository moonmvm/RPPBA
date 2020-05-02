from django.utils.html import format_html
from django.urls import reverse


class RelatedObjectLinkMixin:
    """
    Generate links to related links. To use it specify the link_fields.
    And add '_link' suffix to every field should be clickable in list_display
    """
    link_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.link_fields:
            for field_name in self.link_fields:
                func_name = '{}_link'.format(field_name)
                setattr(self, func_name, self._generate_link_func(field_name))
                func_attr = getattr(self, func_name)
                func_attr.short_description = field_name

    def _generate_link_func(self, field_name):

        def _func(obj, *args, **kwargs):
            related_obj = getattr(obj, field_name)
            if related_obj:
                url_name = 'admin:{}_{}_change'.format(related_obj._meta.app_label, related_obj._meta.model_name)
                url = reverse(url_name, args=[related_obj.pk])
                return format_html('<a href="{}" class="changelink">{}</a>', url, str(related_obj))
            else:
                return None
        return _func
