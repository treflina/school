from django.db import models
from modelcluster.fields import ForeignKey, ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, MultipleChooserPanel
from wagtail.fields import RichTextField
from wagtail.images.models import Image
from wagtail.models import Collection, Orderable, Page
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

    heading = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Nazwa galerii"
    )

    content_panels = Page.content_panels + [
        FieldPanel("heading"),
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
        verbose_name="Zdjęcie",
    )
    alt_attr = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Opis alternatywny",
        help_text="""Opis tekstowy zdjęcia (najczęściej od 5 do 15 słów) mający
        na celu umożliwienie przekazu treści osobom słabowidzącym."""
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("alt_attr")
    ]
