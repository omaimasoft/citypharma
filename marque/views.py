from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .models import Marque


# ============================================================
# PAGINATION SETTINGS
# ============================================================

BRANDS_PER_PAGE = 20
PRODUCTS_PER_PAGE = 12


def paginate_queryset(request, queryset, per_page):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop("page", None)
    pagination_query = query_params.urlencode()

    return page_obj, pagination_query


# ============================================================
# MARQUES LIST
# ============================================================

def liste_marques(request):
    marques_queryset = (
        Marque.objects
        .annotate(
            nbr_produits=Count(
                "products",
                filter=Q(products__active=True),
                distinct=True
            )
        )
        .order_by("nom")
    )

    marques, pagination_query = paginate_queryset(
        request,
        marques_queryset,
        BRANDS_PER_PAGE
    )

    return render(request, "marque/liste_marques.html", {
        "marques": marques,
        "page_obj": marques,
        "pagination_query": pagination_query,
    })


def marque_list(request):
    marques_queryset = (
        Marque.objects
        .annotate(
            nbr_produits=Count(
                "products",
                filter=Q(products__active=True),
                distinct=True
            )
        )
        .order_by("nom")
    )

    marques, pagination_query = paginate_queryset(
        request,
        marques_queryset,
        BRANDS_PER_PAGE
    )

    return render(request, "marque/list.html", {
        "marques": marques,
        "page_obj": marques,
        "pagination_query": pagination_query,
    })


# ============================================================
# MARQUE DETAIL
# ============================================================

def marque_detail(request, marque_id):
    marque = get_object_or_404(Marque, pk=marque_id)

    produits_queryset = (
        marque.products
        .filter(active=True)
        .select_related("marque", "categorie", "sous_categorie")
        .order_by("-id")
    )

    produits, pagination_query = paginate_queryset(
        request,
        produits_queryset,
        PRODUCTS_PER_PAGE
    )

    return render(request, "marque/detail.html", {
        "marque": marque,
        "produits": produits,
        "page_obj": produits,
        "pagination_query": pagination_query,
    })