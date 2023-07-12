from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.documents.models import AbstractDocument, Document
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from .utils import convert_bytes, extract_extension


@register_snippet
class SchoolYearSnippet(models.Model):
    """School year for a snippet."""

    name = models.CharField(max_length=25, verbose_name="rok szkolny")

    panels = [
        FieldPanel("name"),
    ]

    @property
    def urlname(self):
        urlencodedname = self.name.replace("/", "")
        return urlencodedname

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rok szkolny"
        verbose_name_plural = "Rok szkolny"


class CustomDocument(AbstractDocument):
    @property
    def get_extension(self):
        return extract_extension(self.file)

    @property
    def get_size(self):
        return convert_bytes(self.file_size)

    admin_form_fields = Document.admin_form_fields


class IndexPage(Page):
    template = "core/index_page.html"
    desription = "Strona nadrzędna (np. 'O szkole', 'Galerie') - listująca podstrony"

    @property
    def get_child_pages(self):
        return self.get_children().public().live()

    class Meta:
        verbose_name = "Strona nadrzędna"
