from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.admin.panels import FieldPanel
from wagtail.documents.models import AbstractDocument, Document
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from .utils import convert_bytes, extract_extension


@register_snippet
class CategorySnippet(models.Model):
    """News category for a snippet."""

    choices = (
        (0, "różowy"),
        (1, "niebieski"),
        (2, "zielony"),
        (3, "brązowy"),
        (4, "pomarańczowy"),
    )
    name = models.CharField(max_length=25, verbose_name="nazwa kategorii")
    # slug = models.SlugField(max_length=50)
    color = models.IntegerField(
        default=0, choices=choices, verbose_name="Kolor powiązany z kategorią"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("color"),
    ]

    class Meta:
        verbose_name = "Kategoria1"
        verbose_name_plural = "Kategorie"
        ordering = ["name"]

    @classmethod
    def get_default_id(cls):
        category, created = cls.objects.get_or_create(
            name="Galeria",
            defaults=dict(color=3),
        )
        return category.id

    def __str__(self):
        return self.name


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


class PagePaginationMixin:
    """Mixin that handles pagination for index pages giving an ability to use page
    range in case of too many subpages"""
    def pagination(self, request, posts, num=12):
        paginator = Paginator(posts, num)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        index = posts.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]
        return posts, page_range

    class Meta:
        abstract = True


class IndexPage(Page):
    template = "core/index_page.html"
    desription = "Strona nadrzędna (np. 'O szkole', 'Galerie') - listująca podstrony"

    @property
    def get_child_pages(self):
        return self.get_children().public().live()

    class Meta:
        verbose_name = "Strona nadrzędna"
