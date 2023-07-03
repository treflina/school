from datetime import date
from itertools import chain, islice
from operator import attrgetter

from wagtail.models import Page

from gallery.models import GalleryDetailPage
# from events.models import EventsPage
from news.models import NewsCategory, NewsDetailPage


class HomePage(Page):
    template = "home/home_page.html"

    def get_context(self, request, *args, **kwargs):
        """Adding posts to news section"""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts from news and gallery
        news_list = NewsDetailPage.objects.live().public().order_by("-publish_date")
        main_post = news_list.filter(highlight=True).first()
        if not main_post:
            main_post = news_list.first()

        galleries_list = (
            GalleryDetailPage.objects.live().public().order_by("-publish_date")
        )

        for gallery in galleries_list:
            gallery.page_type = "gallery"
            if gallery.gallery_images.filter(highlight=True).first():
                gallery.banner_image = gallery.gallery_images.filter(highlight=True)[
                    0
                ].image
            else:
                if gallery.gallery_images.all():
                    gallery.banner_image = gallery.gallery_images.all()[0].image

        posts = sorted(
            chain(news_list, galleries_list),
            key=attrgetter("publish_date"),
            reverse=True,
        )

        categories = NewsCategory.objects.all().order_by("id")

        if request.GET.get("category", None):
            category = request.GET.get("category")
            posts = list(filter(lambda x: x.category_id == int(category), posts))
            context["active_category"] = categories.filter(id=category).first()

        context["main_post"] = main_post
        context["categories"] = categories
        context["posts"] = [p for p in posts if p != main_post][:6]

        # get upcoming events
        # today = date.today()

        # eventpage = EventsPage.objects.live().first()
        # if eventpage:
        #     allevents = eventpage.events.all().order_by("start_date", "hour")

        #     allevents_days = {}
        #     for e in allevents:
        #         if e.start_date not in allevents_days:
        #             allevents_days[e.start_date] = [e]
        #         else:
        #             allevents_days[e.start_date].append(e)

        #     # for day in allevents_days.values():
        #     #     day.sort(key=lambda x: time(0, 0) if x.hour is None else x.hour)

        #     latest_events_days = dict(
        #         filter(lambda x: x[0] < today, allevents_days.items())
        #     )
        #     upcoming_events_days = dict(
        #         filter(lambda x: x[0] >= today, allevents_days.items())
        #     )
        #     latest_events_days_count = len(latest_events_days)
        #     upcoming_events_days_count = len(upcoming_events_days)

        #     num_diff = 4 - upcoming_events_days_count

        #     if latest_events_days_count + upcoming_events_days_count <= 4:
        #         events = allevents_days
        #     elif num_diff < 0:
        #         events = dict(islice(upcoming_events_days.items(), 4))
        #     else:
        #         latest_dict = dict(list(latest_events_days.items())[-num_diff:])
        #         upcoming_dict = dict(
        #             islice(upcoming_events_days.items(), upcoming_events_days_count)
        #         )
        #         latest_dict.update(upcoming_dict)
        #         events = latest_dict

        #     context["events"] = events

        return context

    class Meta:
        verbose_name = "Strona główna"

from datetime import datetime

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Orderable, Page


class EventsPageForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()

        for form in self.formsets["events"].forms:
            if form.is_valid():
                cleaned_form_data = form.clean()
                end_date = cleaned_form_data.get("end_date")
                start_date = cleaned_form_data.get("start_date")
                if end_date == start_date:
                    form.add_error(
                        "end_date",
                        """Jeśli wydarzenie kończy się w dniu rozpoczęcia,
                            pole pozostaw puste.""",
                    )
        return cleaned_data


class EventsPage(Page):
    template = "home/events_page.html"
    base_form_class = EventsPageForm

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("events", label="")],
            classname="collapsed",
        )
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding posts to news section"""
        context = super().get_context(request, *args, **kwargs)

        allevents = (
            EventsPage.objects.live()
            .first()
            .events.all()
            .order_by("start_date", "hour")
        )
        for e in allevents:
            print(e)

        allevents_months = {}
        for e in allevents:
            date_key = datetime.strptime(
                f"01/{str(e.start_date.month)}/{str(e.start_date.year)}", "%d/%m/%Y"
            ).date()
            if date_key not in allevents_months:
                allevents_months[date_key] = [e]
            else:
                allevents_months[date_key].append(e)

        context["events"] = allevents_months
        return context

    def __str__(self):
        return f"{self.title}"


class Event(Orderable):
    page = ParentalKey(EventsPage, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(
        max_length=200, verbose_name="Nazwa wydarzenia", blank=False, null=True
    )
    start_date = models.DateField(verbose_name="Data")
    end_date = models.DateField(verbose_name="Data zakończenia", blank=True, null=True)
    hour = models.TimeField(verbose_name="Godzina", blank=True, null=True)
    description = models.TextField(
        verbose_name="(Opcjonalnie) Krótki opis", blank=True, null=True
    )

    panels = [
        FieldPanel("name"),
        FieldRowPanel(
            [FieldPanel("start_date"), FieldPanel("end_date"), FieldPanel("hour")]
        ),
        FieldPanel("description"),
    ]

    def __str__(self):
        return f"{self.name} - {self.start_date}"