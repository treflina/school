from datetime import date
from itertools import chain, islice
from operator import attrgetter

from django import forms
from django.db import models
from events.models import EventsPage
from gallery.models import GalleryDetailPage
from news.models import NewsCategory, NewsDetailPage
from streams import blocks
from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail.contrib.routable_page.models import RoutablePageMixin


class HomePage(RoutablePageMixin, Page):
    template = "home/home_page.html"
    parent_page_types = []

    def get_today(self):
        return date.today()

    def get_context(self, request, *args, **kwargs):
        """Adding posts to news section"""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts from news and gallery
        news_list = NewsDetailPage.objects.live().specific().order_by("-publish_date")
        main_post = news_list.filter(highlight=True).first()
        if not main_post:
            main_post = news_list.first()

        galleries_list = (
            GalleryDetailPage.objects.live().specific().order_by("-publish_date")
        )

        posts = sorted(
            chain(news_list, galleries_list),
            key=attrgetter("publish_date"),
            reverse=True,
        )

        categories = NewsCategory.objects.all().order_by("id")

        if request.GET.get("category", None):
            category = request.GET.get("category")
            try:
                posts = list(filter(lambda x: x.category_id == int(category), posts))
                context["active_category"] = categories.filter(id=category).first()
            except ValueError:
                pass

        context["main_post"] = main_post
        context["categories"] = categories
        context["posts"] = [p for p in posts if p != main_post][:6]

        # get upcoming events
        today = self.get_today()

        q = EventsPage.objects.live().all()
        eventpage = q[len(q) - 1] if q else None
        if eventpage:
            allevents = eventpage.events.all().order_by("start_date", "hour")

            allevents_days = {}
            for e in allevents:
                if e.start_date not in allevents_days:
                    allevents_days[e.start_date] = [e]
                else:
                    allevents_days[e.start_date].append(e)

            latest_events_days = dict(
                filter(lambda x: x[0] < today, allevents_days.items())
            )
            upcoming_events_days = dict(
                filter(lambda x: x[0] >= today, allevents_days.items())
            )
            latest_events_days_count = len(latest_events_days)
            upcoming_events_days_count = len(upcoming_events_days)

            num_diff = 4 - upcoming_events_days_count

            if latest_events_days_count + upcoming_events_days_count <= 4:
                events = allevents_days
            elif num_diff < 0:
                events = dict(islice(upcoming_events_days.items(), 4))
            else:
                latest_dict = dict(list(latest_events_days.items())[-num_diff:])
                upcoming_dict = dict(
                    islice(upcoming_events_days.items(), upcoming_events_days_count)
                )
                latest_dict.update(upcoming_dict)
                events = latest_dict

            context["events"] = events

        return context

    class Meta:
        verbose_name = "Strona główna"


class OrdinaryPage(Page):
    template = "home/ordinary_page.html"

    introduction = models.TextField(verbose_name="Tekst", blank=True)
    bold_intro = models.BooleanField(
        verbose_name="Pogrubienie", default=False, null=True
    )
    content = StreamField(
        blocks.RichtextAndTableBlock(),
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name="Treść",
    )

    boolean_widget = forms.RadioSelect(choices=((True, "Tak"), (False, "Nie")))

    content_panels = Page.content_panels + [
        FieldRowPanel(
            [
                FieldPanel("introduction", classname="col10", disable_comments=True),
                FieldPanel("bold_intro", classname="col2", widget=boolean_widget),
            ],
            heading="Wprowadzenie",
        ),
        FieldPanel("content"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("content"),
    ]

    class Meta:  # noqa
        verbose_name = "Podstrona"
        verbose_name_plural = "Podstrony"


class TeachersPage(Page):
    template = "home/teachers_page.html"

    year = models.ForeignKey(
        "core.SchoolYearSnippet",
        verbose_name="Rok szkolny",
        max_length=10,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    introduction = models.TextField(verbose_name="Wprowadzenie", null=True, blank=True)
    content = StreamField(
        [("info", blocks.ObjectAndDescriptionBlock())],
        use_json_field=True,
        verbose_name="Nauczyciele",
        null=True,
        blank=True,
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Zdjęcie",
    )

    content_panels = Page.content_panels + [
        FieldPanel("year"),
        FieldPanel("introduction"),
        FieldPanel("content"),
        FieldPanel("image")
    ]
