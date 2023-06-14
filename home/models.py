from django.db import models

from wagtail.models import Page

from datetime import date

from django.db import models
from django.shortcuts import render
from django.http import Http404

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from modelcluster.fields import ParentalKey

from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.models import Collection
from wagtail.fields import StreamField
from wagtail.models import Page, Orderable

from wagtail import blocks as wagtail_blocks
from . import blocks


class HomePage(Page):
    template = "home/home_page.html"


    class Meta:
        verbose_name = "Strona główna"

class NewsPage(Page):
    template="home/news_page.html"
    
    accordion_content = StreamField(
    [
        ("cards", blocks.AccordionBlock()),
    ],
    null=True,
    blank=True,
    use_json_field=True,
    verbose_name="Aktualności"
)
    content_panels = Page.content_panels + [
        FieldPanel("accordion_content"),
]
    class Meta:
        verbose_name = "Aktualności"


