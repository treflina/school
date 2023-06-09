from django.db import models

from modelcluster.fields import ParentalKey, ForeignKey
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable, Collection
from wagtail.admin.panels import FieldPanel, MultipleChooserPanel
from wagtail.images.models import Image



class GalleryListingPage(Page):
    template = "gallery/gallery_listing_page.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = ["gallery.GalleryDetailPage"]
    password_required_template = "gallery/password_required.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        galleries = (
            GalleryListingPage.get_children(self)
            .specific()
            .live()
            .order_by("-first_published_at")
        )
        context["galleries"] = galleries
        return context

    class Meta:
        verbose_name = "Galeria - strona nadrzędna"


class GalleryDetailPage(Page):
    template = "gallery/gallery_detail_page.html"
    subpage_types = []
    parent_page_types = ["gallery.GalleryListingPage"]
    # password_required_template = "gallery/password_required.html"


    content_panels = Page.content_panels + [
        MultipleChooserPanel(
            "gallery_images",
            label="Zdjęcia",
            chooser_field_name="image",
        ),
    ]

    class Meta:
        verbose_name = "Galeria zdjęć"


class GalleryImage(Orderable):
    page = ParentalKey(
        GalleryDetailPage, on_delete=models.CASCADE, related_name="gallery_images"
    )

    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="+", verbose_name="zdjęcie"
    )

    panels = [
        FieldPanel("image"),
    ]


from wagtail_multi_upload.edit_handlers import MultipleImagesPanel


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        #Change this
        # InlinePanel('gallery_images', label="Gallery images"),
        # to this
        MultipleImagesPanel("gallery_images", label="Gallery images", image_field_name="image"),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]