from django.db import models
from django.utils.timezone import now
from modelcluster.fields import ParentalKey
from news.models import NewsCategory
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail_multi_upload.edit_handlers import MultipleImagesPanel


class GalleryIndexPage(Page):
    template = "gallery/gallery_index_page.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = ["gallery.GalleryDetailPage"]
    password_required_template = "gallery/password_required.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        galleries = (
            GalleryIndexPage.get_children(self)
            .specific()
            .live()
            .order_by("-first_published_at")
        )
        context["galleries"] = galleries
        return context

    class Meta:
        verbose_name = "Lista galerii zdjęć"


class GalleryDetailPage(Page):
    template = "gallery/gallery_detail_page.html"
    subpage_types = []
    parent_page_types = ["gallery.GalleryIndexPage"]
    # password_required_template = "gallery/password_required.html"

    main_text = RichTextField(
        blank=True,
        null=True,
        verbose_name="Opis galerii",
        help_text="Opcjonalny dodatkowy opis galerii.",
    )

    publish_date = models.DateField(
        blank=True,
        null=True,
        default=now,
        verbose_name="Data publikacji",
        help_text="""Data publikacji wyświetlana na stronie.""",
    )

    category = models.ForeignKey(
        NewsCategory,
        null=True,
        on_delete=models.SET_NULL,
        default=NewsCategory.get_default_id,
    )

    content_panels = Page.content_panels + [
        FieldPanel("publish_date"),
        FieldPanel("main_text"),
        MultiFieldPanel(
            [
                MultipleImagesPanel(
                    "gallery_images", label="", image_field_name="image"
                ),
            ],
            heading="Zdjęcia",
        ),
    ]

    class Meta:
        verbose_name = "Galeria zdjęć"
        verbose_name_plural = "Galerie zdjęć"


class GalleryImage(Orderable):
    page = ParentalKey(
        GalleryDetailPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="",
    )
    alt_attr = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Opis alternatywny",
        help_text="""Opis tekstowy zdjęcia (najczęściej od 5 do 15 słów) mający
        na celu umożliwienie przekazu treści osobom słabowidzącym.""",
    )
    highlight = models.BooleanField(
        default=False,
        verbose_name="Zdjęcie główne",
        help_text="""Wybrane zdjęcie będzie wyświetlone w wizytówce galerii""",
    )

    panels = [
        FieldRowPanel([FieldPanel("image"), FieldPanel("highlight")]),
        FieldPanel("alt_attr")
        ]
