from datetime import date

from django.db import models
from django.http import Http404
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail import blocks as wagtail_blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Collection, Orderable, Page

from . import blocks


class HomePage(Page):
    template = "home/home_page.html"

    class Meta:
        verbose_name = "Strona główna"


class NewsPage(Page):
    template = "home/news_page.html"

    accordion_content = StreamField(
        [
            ("cards", blocks.AccordionBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name="Aktualności",
    )
    content_panels = Page.content_panels + [
        FieldPanel("accordion_content"),
    ]
