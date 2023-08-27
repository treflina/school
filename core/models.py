from PIL import Image as PILImage

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.documents.models import AbstractDocument, Document
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index

from .utils import convert_bytes, extract_extension

from streams import blocks


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
    color = models.IntegerField(
        default=0, choices=choices, verbose_name="Kolor powiązany z kategorią"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("color"),
    ]

    class Meta:
        verbose_name = "Kategoria"
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


class CustomImage(AbstractImage):
    admin_form_fields = Image.admin_form_fields

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if (self.width > 1200 or self.height > 1200) and self.collection.name != "Zdjęcia - rozmiar oryginalny":
            img = PILImage.open(self.file.path)
            img.thumbnail((1200, 1200))
            width, height = img.size
            img.save(self.file.path)

            if self.width != width or self.height != height:
                self.width = width
                self.height = height
                self.file_size = self.file.size
                self.save(update_fields=["width", "height", "file_size"])


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


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
    parent_page_types = ["home.HomePage"]
    page_description = """Np. 'O szkole', 'Dla rodziców' - używana do stworzenia rodzica
                dla innych podstron"""

    @property
    def get_child_pages(self):
        return self.get_children().public().live()

    class Meta:
        verbose_name = "Strona nadrzędna"


class OrdinaryPage(Page):
    template = "core/ordinary_page.html"
    parent_page_types = ["core.IndexPage", "home.HomePage"]
    content = StreamField(
        blocks.RichtextAndTableBlock(),
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name="Treść",
    )

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]

    search_fields = Page.search_fields + [
        index.RelatedFields("content", [index.SearchField("docs")]),
    ]

    class Meta:  # noqa
        verbose_name = "Podstrona - zwykła"
        verbose_name_plural = "Zwykłe podstrony"


class TeachersPage(Page):
    template = "core/teachers_page.html"
    parent_page_types = ["core.IndexPage"]
    page_description = """Używana np. do stworzenia
             zakładek 'Grono pedagogiczne', 'RSU'"""

    year = models.ForeignKey(
        "core.SchoolYearSnippet",
        verbose_name="Rok szkolny",
        max_length=10,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    introduction = models.TextField(verbose_name="Wprowadzenie", null=True, blank=True)
    content = StreamField(
        [("info", blocks.ObjectAndDescriptionBlock())],
        use_json_field=True,
        verbose_name="Nauczyciele",
        null=True,
        blank=True,
    )
    image = models.ForeignKey(
        "core.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="",
    )
    alt_attr = models.CharField(
        "Opis alternatywny", max_length=255, null=True, blank=True
    )
    additional_content = StreamField(
        blocks.ContentBlock(), use_json_field=True, null=True, blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("year"),
        FieldPanel("introduction"),
        FieldPanel("content"),
        MultiFieldPanel(
            [FieldPanel("image"), FieldPanel("alt_attr")], heading="Zdjęcie główne"
        ),
        FieldPanel("additional_content", heading="Dodatkowy tekst, zdjęcia, tabele"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("content"),
    ]

    class Meta:  # noqa
        verbose_name = """Podstrona typu przedmiot-bardzo krótki opis
                 (np. imię i nazwisko)"""
        verbose_name_plural = "Podstrony typu przedmiot-opis"


class ContactPage(Page):
    template = "core/contact_page.html"
    max_count = 1
    subpage_types = []
    parent_page_types = ["home.HomePage"]

    name = models.CharField("nazwa", max_length=255, blank=False, null=True)
    address1 = models.CharField("ulica, numer", max_length=255, blank=False, null=True)
    address2 = models.CharField(
        "kod pocztowy, miejscowość", max_length=255, blank=False, null=True
    )
    phone = models.CharField("telefon", max_length=60, blank=False, null=True)
    fax = models.CharField("fax", max_length=30, blank=True, null=True)
    email = models.EmailField("e-mail", blank=False, null=True)

    additional_info = RichTextField(
        "Dodatkowe informacje",
        features=["bold", "hr", "link", "document-link"],
    )

    image = models.ForeignKey(
        "core.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="",
    )
    alt_attr = models.CharField(
        "Opis alternatywny", max_length=255, null=True, blank=True
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("address1"),
                FieldPanel("address2"),
                FieldPanel("phone"),
                FieldPanel("fax"),
                FieldPanel("email"),
            ],
            heading="Podstawowe dane kontaktowe",
        ),
        FieldPanel("additional_info", heading="Dodatkowe informacje"),
        MultiFieldPanel(
            [FieldPanel("image"), FieldPanel("alt_attr")], heading="Zdjęcie"
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("additional_info"),
    ]

    class Meta:  # noqa
        verbose_name = "Kontakt"
        verbose_name_plural = "Kontakt"

