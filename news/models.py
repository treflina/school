from itertools import chain
from operator import attrgetter

from core.models import CategorySnippet, PagePaginationMixin
from django.db import models
from django.utils.timezone import now
from gallery.models import GalleryDetailPage
from modelcluster.fields import ParentalKey
from streams import blocks
from wagtail.admin.panels import FieldPanel  # MultipleChooserPanel,
from wagtail.admin.panels import MultiFieldPanel, PageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail_multi_upload.edit_handlers import MultipleImagesPanel


class NewsIndexPage(PagePaginationMixin, RoutablePageMixin, Page):
    """News listing page model."""

    template = "news/news_index_page.html"
    subpage_types = ["news.NewsDetailPage"]
    parent_page_types = ["home.HomePage"]
    max_count = 1
    search_fields = Page.search_fields

    @property
    def get_child_pages(self):
        return self.get_children().public().live()

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)

        news = (
            NewsDetailPage.objects.live()
            .specific()
            .order_by("-publish_date", "-first_published_at")
        )
        galleries_list = (
            GalleryDetailPage.objects.live()
            .specific()
            .order_by("-publish_date", "-first_published_at")
        )

        all_news = sorted(
            chain(news, galleries_list),
            key=attrgetter("publish_date"),
            reverse=True,
        )

        # Add filtering news by category
        categories = CategorySnippet.objects.all().order_by("id")
        context["categories"] = categories

        if request.GET.get("category", None):
            category = request.GET.get("category")
            try:
                all_news = list(
                    filter(lambda x: x.category_id == int(category), all_news)
                )
                context["active_category"] = categories.filter(id=category).first()
            except ValueError:
                pass

        context["posts"], context["page_range"] = self.pagination(request, all_news)
        return context

    class Meta:  # noqa
        verbose_name = "Wszystkie aktualności"
        verbose_name_plural = "Wszystkie aktualności"


class NewsDetailPage(Page):
    """Detail page for news content."""

    page_description = "Strona służąca zamieszczeniu nowego artykułu w Aktualnościach"

    subpage_types = []
    parent_page_types = ["news.NewsIndexPage"]

    category = models.ForeignKey(
        "core.CategorySnippet",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Kategoria",
    )

    banner_image = models.ForeignKey(
        "core.CustomImage",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Zdjęcie główne",
        help_text="""Preferowana orientacja pozioma.""",
    )
    checkered = models.BooleanField(
        verbose_name="Tło zdjęcia w kratkę",
        default=False,
        help_text="""Wyśrodkowuje zdjęcie na stronie głównej i dodaje efekt kratki.
        Przydatne do zdjęć o wysokości mniejszej niż tekst wprowadzający.""",
    )
    alt_attr = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Opis alternatywny",
        help_text="""Proszę opisać co przedstawia zdjęcie. Pole nie powinno być puste
        (wymóg dostępności cyfrowej stron internetowych instytucji publicznych). Jeżeli zdjęcie
        zawiera informację tekstową, musi być ona zawarta również w tekstowej części artykułu lub ewentualnie w opisie
        alternatywnym. To samo dotyczy pozostałych zdjęć w artykule. Więcej informacji:
        https://www.uke.gov.pl/blog/tekst-alternatywny-do-grafik-i-zdjec-czyli-kilka-slow-o-altach,96.html""",
    )
    main_text = RichTextField(
        blank=False,
        null=True,
        verbose_name="Tekst główny",
        help_text="Tekst wprowadzający. Preferowana długość odpowiadająca wysokości zdjęcia głównego.",
        features=[
            "bold",
            "italic",
            "center",
            "right",
            "ol",
            "ul",
            "hr",
            "link",
            "document-link",
        ],
    )
    body = StreamField(
        blocks.RichtextAndTableBlock(),
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name="Dalszy tekst (w tym zdjęcia na pełną szerokość ekranu), tabele, dokumenty",
    )
    highlight = models.BooleanField(
        default=True,
        verbose_name="Wyróżnienie na stronie głównej",
        help_text="""Wyświetl wprowadzaną aktualność jako pierwszą informację na głównej
        stronie.""",
    )
    publish_date = models.DateField(
        blank=True,
        null=True,
        default=now,
        verbose_name="Data publikacji",
        help_text="""Data publikacji wyświetlana na stronie.""",
    )
    author = models.CharField(
        "autor",
        max_length=80,
        blank=True,
        null=True,
        help_text="""Podaj autora, jeśli chcesz żeby ta informacja była wyświetlona
            na stronie""",
    )
    button_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Link do galerii zdjęć",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("category"),
                FieldPanel("highlight"),
                FieldPanel("publish_date"),
                FieldPanel("author"),
            ],
            heading="Informacje o artykule",
        ),
        MultiFieldPanel(
            [
                # FieldPanel("heading"),
                FieldPanel("banner_image"),
                FieldPanel("alt_attr"),
                FieldPanel("checkered"),
                FieldPanel("main_text"),
                FieldPanel("body"),
            ],
            heading="Treść",
        ),
        MultiFieldPanel(
            [
                PageChooserPanel("button_cta", "gallery.GalleryDetailPage"),
                MultipleImagesPanel(
                    "gallery_images",
                    label="Zdjęcia",
                    image_field_name="image",
                    help_text="Wybrane zdjęcia zostaną zamieszczone na końcu artykułu.",
                ),
            ],
            heading="""Link do strony z galerią zdjęć lub/i mini galeria
            na końcu artykułu.""",
            help_text="""Możesz wybrać link do utworzonej wcześniej strony
            z galerią zdjęć lub zamieścić zdjęcia, które będą wyświetlone na końcu
            artykułu w postaci mini galerii""",
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("main_text"),
        index.SearchField("body"),
        index.FilterField("publish_date"),
    ]

    class Meta:  # noqa
        verbose_name = "Artykuł"
        verbose_name_plural = "Artykuły"

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)

        news = (
            NewsDetailPage.objects.live()
            .filter(publish_date__lte=self.publish_date)
            .exclude(id=self.id)
        )
        galleries = GalleryDetailPage.objects.live().filter(
            publish_date__lte=self.publish_date
        )
        all_posts = sorted(
            chain(news, galleries),
            key=attrgetter("publish_date"),
            reverse=True,
        )[:10]

        context["prev_news"] = all_posts

        return context


class MiniGalleryImage(Orderable):
    page = ParentalKey(
        NewsDetailPage, on_delete=models.CASCADE, related_name="gallery_images"
    )

    image = models.ForeignKey(
        "core.CustomImage",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Zdjęcie",
    )
    alt_attr = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Opis alternatywny",
        help_text="""Opis tekstowy zdjęcia (najczęściej od 5 do 15 słów). Proszę nie pozostawiać bez opisu""",
    )

    panels = [FieldPanel("image"), FieldPanel("alt_attr")]


NewsDetailPage._meta.get_field(
    "title"
).help_text = """Jeśli tytuł strony nie jest
unikalny, przejdź do zakładki Promocja SEO (powyżej) i zmień pole slug tak, żeby się nie
powtarzało (np.dopisując kolejną cyfrę)"""
