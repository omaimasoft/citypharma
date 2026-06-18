from .models import Cart, Categorie


def cart_counter(request):
    count = 0
    cart = None

    try:
        if request.user.is_authenticated:
            cart = (
                Cart.objects
                .filter(user=request.user, is_ordered=False)
                .prefetch_related('store_items')
                .first()
            )
        else:
            session_key = request.session.session_key

            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            cart = (
                Cart.objects
                .filter(user__isnull=True, session_key=session_key, is_ordered=False)
                .prefetch_related('store_items')
                .first()
            )

        if cart:
            count = sum(item.quantity for item in cart.store_items.all())

    except Exception:
        count = 0

    return {
        'cart_items_count': count
    }


def menu_categories(request):
    categories = (
        Categorie.objects
        .filter(active=True)
        .prefetch_related('subcategories')
        .order_by('ordre', 'nom')
    )

    return {
        'menu_categories': categories
    }