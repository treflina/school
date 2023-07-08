from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.timezone import now
from modelcluster.fields import ParentalKey
from streams import blocks
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    MultipleChooserPanel,
    PageChooserPanel,
)
from wagtail.fields import RichTextField, StreamField

# from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.models import Orderable, Page
from wagtail.contrib.routable_page.models import RoutablePageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class NewsCategory(models.Model):
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
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"
        ordering = ["name"]

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name, allow_unicode=True)
    #     super().save(self, *args, **kwargs)
    @classmethod
    def get_default_id(cls):
        category, created = cls.objects.get_or_create(
            name='Galeria',
            defaults=dict(color=3),
        )
        return category.id

    def __str__(self):
        return self.name


class NewsIndexPage(RoutablePageMixin, Page):
    """News listing page model."""

    template = "news/news_index_page.html"
    subpage_types = ["news.NewsDetailPage"]
    parent_page_types = ["home.HomePage"]

    @property
    def get_child_pages(self):
        return self.get_children().public().live()
        # return self.get_children().public().live().values("id", "title", "slug")

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)

        all_news = (
            NewsDetailPage.objects.live().public().order_by("-publish_date")
        )
        # Add filtering news by category
        categories = NewsCategory.objects.all().order_by("id")
        context["categories"] = categories

        if request.GET.get("category", None):
            category = request.GET.get("category")
            try:
                all_news = list(filter(lambda x: x.category_id == int(category), all_news))
                context["active_category"] = categories.filter(id=category).first()
            except ValueError:
                pass

        context['posts'], context['page_range'] = self.pagination(request, all_news)
        print('context', context)
        return context

    def pagination(self, request, posts):
        paginator = Paginator(posts, 1)
        page = request.GET.get('page')
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
        print('\n', posts, '\n', page_range)
        return posts, page_range


    class Meta:  # noqa
        verbose_name = "Wszystkie aktualności"
        verbose_name_plural = "Wszystkie aktualności"


class NewsDetailPage(Page):
    """Detail page for news content."""

    page_description = "Strona służąca zamieszczeniu nowego artykułu w Aktualnościach"

    subpage_types = []
    parent_page_types = ["news.NewsIndexPage"]

    # heading = models.CharField(
    #     max_length=90, verbose_name="Nagłówek", blank=False, null=True
    # )
    category = models.ForeignKey(
        "news.NewsCategory",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Kategoria",
    )

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Zdjęcie główne",
    )
    alt_attr = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Opis alternatywny",
        help_text="""Opis tekstowy zdjęcia głównego (najczęściej od 5 do 15 słów) mający
        na celu umożliwienie przekazu treści osobom słabowidzącym.""",
    )
    main_text = RichTextField(
        blank=False,
        null=True,
        verbose_name="Tekst główny",
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
        blocks.ContentBlock(),
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name="Dodatkowe teksty, zdjęcia, tabele",
    )
    highlight = models.BooleanField(
        default=False,
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
                # FieldPanel("heading"),
                FieldPanel("banner_image"),
                FieldPanel("alt_attr"),
                FieldPanel("main_text"),
                FieldPanel("body"),
            ],
            heading="Treść",
        ),
        MultiFieldPanel(
            [
                FieldPanel("category"),
                FieldPanel("highlight"),
                FieldPanel("publish_date"),
            ],
            heading="Informacje o artykule",
        ),
        MultiFieldPanel(
            [
                PageChooserPanel("button_cta"),
                MultipleChooserPanel(
                    "gallery_images",
                    label="Zdjęcia",
                    chooser_field_name="image",
                    help_text="Wybrane zdjęcia zostaną zamieszczone na końcu artykułu.",
                ),
            ],
            heading="""Opcjonalnie: link do strony z galerią zdjęć lub mini galeria
            na końcu artykułu.""",
            help_text="""Możesz wybrać link do utworzonej wcześniej strony
            z galerią zdjęć lub zamieścić kilka zdjęć, które będą wyświetlone na końcu
            artykułu w postaci mini galerii""",
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('main_text'),
        index.SearchField('body'),
        # index.FilterField('date'),
    ]

    class Meta:  # noqa
        verbose_name = "Artykuł"
        verbose_name_plural = "Artykuły"


class MiniGalleryImage(Orderable):
    page = ParentalKey(
        NewsDetailPage, on_delete=models.CASCADE, related_name="gallery_images"
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Zdjęcie",
    )
    alt_attr = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Opis alternatywny",
        help_text="""Opis tekstowy zdjęcia (najczęściej od 5 do 15 słów) mający
        na celu umożliwienie przekazu treści osobom słabowidzącym.""",
    )

    panels = [FieldPanel("image"), FieldPanel("alt_attr")]


NewsDetailPage._meta.get_field(
    "title"
).help_text = """Jeśli tytuł strony nie jest
unikalny, przejdź do zakładki Promocja SEO (powyżej) i zmień pole slug tak, żeby się nie
powtarzało (np.dopisując kolejną cyfrę)"""
