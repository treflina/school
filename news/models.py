from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.text import slugify
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
from wagtail.snippets.models import register_snippet


@register_snippet
class NewsCategory(models.Model):
    """News category for a snippet."""

    name = models.CharField(max_length=25, verbose_name="nazwa kategorii")
    slug = models.SlugField(max_length=50)

    panels = [
        FieldPanel("name"),
    ]

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(self, *args, **kwargs)

    def __str__(self):
        return self.name


class NewsIndexPage(Page):
    """News listing page model."""

    template = "news/news_index_page.html"

    class Meta:  # noqa
        verbose_name = "Wszystkie aktualności"
        verbose_name_plural = "Wszystkie aktualności"

    @property
    def get_child_pages(self):
        return self.get_children().public().live()
        # return self.get_children().public().live().values("id", "title", "slug")

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = (
            NewsDetailPage.objects.live().public().order_by("-first_published_at")
        )

        if request.GET.get("tag", None):
            tags = request.GET.get("tag")
            all_posts = all_posts.filter(tags__slug__in=[tags])

        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 2)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["posts"] = posts
        context["categories"] = NewsCategory.objects.all()
        return context


class NewsDetailPage(Page):
    """Detail page for news content."""

    subpage_types = []
    parent_page_types = ["news.NewsIndexPage"]

    heading = models.CharField(
        max_length=90, verbose_name="Nagłówek", blank=False, null=True
    )
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
    main_text = RichTextField(
        blank=False,
        null=True,
        verbose_name="Tekst główny",
        features=[
            "bold",
            "italic",
            "center",
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
        verbose_name="Data publikacji",
        help_text="""Możesz zmienić datę, jeżeli pole pozostawisz puste,
        w artykule pojawi się data pierwszej publikacji artykułu.""")
    button_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Link do galerii zdjęć",
    )

    #     accordion_content = StreamField(
    #     [
    #         ("cards", blocks.AccordionBlock()),
    #     ],
    #     null=True,
    #     blank=True,
    #     use_json_field=True,
    #     verbose_name="Aktualności"
    # )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("heading"),
                FieldPanel("banner_image"),
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
                ),
            ],
            heading="""Opcjonalnie: link do strony z galerią zdjęć lub mini galeria
            pod artykułem""",
            help_text="""Możesz wybrać link do utworzonej wcześniej strony
            z galerią zdjęć lub zamieścić kilka zdjęć, które będą wyświetlone na końcu
            artykułu w postaci mini galerii""",
        ),
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
        verbose_name="zdjęcie",
    )

    panels = [
        FieldPanel("image"),
    ]
