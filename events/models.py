from datetime import datetime

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.models import Orderable, Page
from wagtail.search import index


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
    template = "events/events_page.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = []
    max_count = 1
    base_form_class = EventsPageForm

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("events", label="")],
            classname="collapsed",
        )
    ]
    search_fields = Page.search_fields + [
        index.RelatedFields(
            "events",
            [
                index.SearchField("name"),
            ],
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

    class Meta:
        verbose_name = "Wydarzenia"


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
    link_to_details = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Link do strony ze szczegółami wydarzenia np. w Aktualnościach"
    )

    panels = [
        FieldPanel("name"),
        FieldRowPanel(
            [FieldPanel("start_date"), FieldPanel("end_date"), FieldPanel("hour")]
        ),
        FieldPanel("description"),
        PageChooserPanel("link_to_details"),
    ]

    def __str__(self):
        return f"{self.name} - {self.start_date}"
