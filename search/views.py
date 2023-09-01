from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from wagtail.contrib.search_promotions.models import Query
from wagtail.models import Page


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)
        query.add_hit()

        num_results = len(search_results)
        if num_results == 1:
            result = f"{num_results} wynik"
        elif num_results in [2, 3, 4]:
            result = f"{num_results} wyniki"
        elif num_results > 4:
            result = f"{num_results} wyników"
        else:
            result = None
    else:
        search_results = Page.objects.none()
        result = "0 wyników"

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "result": result,
        },
    )
