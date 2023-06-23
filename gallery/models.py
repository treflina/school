from django.db import models
from modelcluster.fields import ForeignKey, ParentalKey
from wagtail.admin.panels import FieldPanel, MultipleChooserPanel
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
        MultipleImagesPanel(
            "gallery_images", label="zdjęcie", image_field_name="image"
        ),
    ]


class GalleryImage(Orderable):
    page = ParentalKey(
        GalleryDetailPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+", verbose_name=""
    )

    panels = [
        FieldPanel("image"),
    ]
