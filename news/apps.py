from django.apps import AppConfig
from django.db.models import ForeignKey


class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news"

    def ready(self):
        from wagtail.admin.forms.models import register_form_field_override
        from core.models import CategorySnippet

        queryset = CategorySnippet.objects.exclude(name="Galeria")

        register_form_field_override(
            ForeignKey, to=CategorySnippet, override={"queryset": queryset}
        )
