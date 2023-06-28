from wagtail.models import Page

from news.models import NewsCategory, NewsDetailPage


class HomePage(Page):
    template = "home/home_page.html"

    def get_context(self, request, *args, **kwargs):
        """Adding posts to news section"""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts

        posts = NewsDetailPage.objects.live().public().order_by("-publish_date")
        categories = NewsCategory.objects.all().order_by("id")

        main_post = posts.filter(highlight=True).first()
        if not main_post:
            main_post = posts.first()

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
