from itertools import chain
from operator import attrgetter

from gallery.models import GalleryDetailPage
from news.models import NewsCategory, NewsDetailPage
from wagtail.models import Page


class HomePage(Page):
    template = "home/home_page.html"

    def get_context(self, request, *args, **kwargs):
        """Adding posts to news section"""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts

        news_list = NewsDetailPage.objects.live().public().order_by("-publish_date")
        main_post = news_list.filter(highlight=True).first()
        if not main_post:
            main_post = news_list.first()

        galleries_list = (
            GalleryDetailPage.objects.live().public().order_by("-publish_date")
        )

        posts = sorted(
            chain(news_list, galleries_list),
            key=attrgetter("publish_date"),
            reverse=True,
        )
        categories = NewsCategory.objects.all().order_by("id")

        if request.GET.get("category", None):
            category = request.GET.get("category")
            posts = posts.filter(category_id=category)
            context["active_category"] = categories.filter(id=category).first()

        context["main_post"] = main_post
        context["categories"] = categories
        context["posts"] = [p for p in posts if p != main_post][:6]
        return context

    class Meta:
        verbose_name = "Strona główna"
