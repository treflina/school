from datetime import date
from itertools import chain, islice
from operator import attrgetter

from core.models import CategorySnippet, LuckyNumberSnippet
from events.models import EventsPage
from gallery.models import GalleryDetailPage
from news.models import NewsDetailPage
from wagtail.models import Page


class HomePage(Page):
    template = "home/home_page.html"
    parent_page_types = ["wagtailcore.Page"]
    max_count = 1

    def get_today(self):
        return date.today()

    def get_context(self, request, *args, **kwargs):
        """Adding posts to news section"""
        context = super().get_context(request, *args, **kwargs)

        today = self.get_today()

        # Get all posts from news and gallery
        news_list = (
            NewsDetailPage.objects.live()
            .specific()
            .order_by("-publish_date", "-first_published_at")
        )
        main_post = news_list.filter(highlight=True).first()
        if not main_post:
            main_post = news_list.first()

        galleries_list = (
            GalleryDetailPage.objects.filter(on_main_page=True)
            .live()
            .specific()
            .order_by("-publish_date", "-first_published_at")
        )

        posts = sorted(
            chain(news_list, galleries_list),
            key=attrgetter("publish_date"),
            reverse=True,
        )

        categories = CategorySnippet.objects.all().order_by("id")

        if request.GET.get("category", None):
            category = request.GET.get("category")
            try:
                posts = list(filter(lambda x: x.category_id == int(category), posts))
                context["active_category"] = categories.filter(id=category).first()
            except ValueError:
                pass

        context["main_post"] = main_post
        context["categories"] = categories
        context["lucky_number"] = LuckyNumberSnippet.objects.filter(date=today).last()
        context["posts"] = [p for p in posts if p != main_post][:6]

        # get upcoming events

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

    search_fields = Page.search_fields

    class Meta:  # noqa
        verbose_name = "Strona główna"
