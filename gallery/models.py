from core.models import PagePaginationMixin, SchoolYearSnippet
# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.timezone import now
from modelcluster.fields import ParentalKey
from news.models import NewsCategory
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail_multi_upload.edit_handlers import MultipleImagesPanel


class GalleryIndexPage(PagePaginationMixin, RoutablePageMixin, Page):
    template = "gallery/gallery_index_page.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = ["gallery.GalleryDetailPage"]
    password_required_template = "gallery/password_required.html"

    search_fields = Page.search_fields

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        galleries = (
            GalleryDetailPage.objects.specific().live().order_by("-publish_date")
        )

        context["years"] = SchoolYearSnippet.objects.all()

        if request.GET.get("year", None):
            urlyear = request.GET.get("year")
            if len(urlyear) >= 4:
                year = f"{urlyear[:4]}/{urlyear[4:]}"
            try:
                galleries = list(filter(lambda x: x.year.name == year, galleries))
                context["active_year"] = year
            except ValueError:
                pass
        context["posts"], context["page_range"] = self.pagination(
            request, galleries
        )
        return context

    class Meta:
        verbose_name = "Lista galerii zdjęć"


class GalleryDetailPage(PagePaginationMixin, Page):
    template = "gallery/gallery_detail_page.html"
    subpage_types = []
    parent_page_types = ["gallery.GalleryIndexPage"]

    main_text = RichTextField(
        blank=True, null=True, verbose_name="Opis galerii", features=[]
    )

    publish_date = models.DateField(
        blank=True,
        null=True,
        default=now,
        verbose_name="Data publikacji",
        help_text="""Data publikacji wyświetlana na stronie.""",
    )

    year = models.ForeignKey(
        "core.SchoolYearSnippet",
        blank=False,
        null=True,
        verbose_name="Rok szkolny",
        on_delete=models.SET_NULL,
        related_name="+",
    )

    category = models.ForeignKey(
        "news.NewsCategory",
        null=True,
        on_delete=models.SET_NULL,
        default=NewsCategory.get_default_id,
    )

    @property
    def get_banner_image(self):
        img = self.gallery_images.filter(highlight=True).last()
        if img is None:
            img = self.gallery_images.last()
        return img

    content_panels = Page.content_panels + [
        FieldRowPanel([FieldPanel("publish_date"), FieldPanel("year")]),
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

    search_fields = Page.search_fields + [index.SearchField("main_text")]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        gallery_images = (
            GalleryImage.objects.filter(page_id=self.id)
        )
        context["posts"], context["page_range"] = self.pagination(
            request, gallery_images, num=18
        )
        return context

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
        null=True,
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
        FieldPanel("alt_attr"),
    ]

    def __str__(self):
        return self.image.title
