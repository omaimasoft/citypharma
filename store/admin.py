from django.contrib import admin, messages
from django.utils.html import format_html

from .models import (
    Categorie,
    SousCategorie,
    Product,
    ProductImage,
    OffreSpeciale,
    Promotion,
    PromotionItem,
    Cart,
    CartItem,
    AvisClient,
    CustomerOrder,
    CustomerOrderItem,
)


# ============================================================
# HELPERS
# ============================================================

def badge(text, bg="#036d70", color="#fff", min_width="70px"):
    return format_html(
        '<span style="background:{}; color:{}; padding:5px 10px; '
        'border-radius:999px; font-size:11px; font-weight:700; '
        'display:inline-flex; align-items:center; justify-content:center; '
        'white-space:nowrap; min-width:{}; line-height:1;">{}</span>',
        bg, color, min_width, text
    )


def image_preview_html(image, max_width="180px"):
    if image:
        return format_html(
            '<img src="{}" style="max-width:{}; border-radius:12px; '
            'border:1px solid #ddd; padding:4px; background:#fff;" />',
            image.url,
            max_width
        )

    return format_html('<span style="color:#999;">Aucune image</span>')


# ============================================================
# CATEGORIES
# ============================================================

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "slug",
        "ordre",
        "active",
        "image_preview",
    )

    list_editable = (
        "ordre",
        "active",
    )

    search_fields = (
        "nom",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("nom",),
    }

    ordering = (
        "ordre",
        "nom",
    )

    readonly_fields = (
        "image_preview",
    )

    fieldsets = (
        ("Informations", {
            "fields": (
                "nom",
                "slug",
                "active",
            )
        }),
        ("Organisation", {
            "fields": (
                "ordre",
            )
        }),
        ("Image", {
            "fields": (
                "image",
                "image_preview",
            )
        }),
    )

    @admin.display(description="Aperçu image")
    def image_preview(self, obj):
        return image_preview_html(obj.image, "180px")


@admin.register(SousCategorie)
class SousCategorieAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "parent",
        "slug",
        "ordre",
        "active",
        "image_preview",
    )

    list_filter = (
        "parent",
        "active",
    )

    list_editable = (
        "ordre",
        "active",
    )

    search_fields = (
        "nom",
        "slug",
        "parent__nom",
    )

    prepopulated_fields = {
        "slug": ("nom",),
    }

    ordering = (
        "parent__ordre",
        "ordre",
        "nom",
    )

    readonly_fields = (
        "image_preview",
    )

    autocomplete_fields = (
        "parent",
    )

    fieldsets = (
        ("Informations", {
            "fields": (
                "parent",
                "nom",
                "slug",
                "active",
            )
        }),
        ("Organisation", {
            "fields": (
                "ordre",
            )
        }),
        ("Image", {
            "fields": (
                "image",
                "image_preview",
            )
        }),
    )

    @admin.display(description="Aperçu image")
    def image_preview(self, obj):
        return image_preview_html(obj.image, "180px")


# ============================================================
# PRODUCTS
# ============================================================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "image_tag",
        "nom_styled",
        "categorie_styled",
        "sous_categorie_styled",
        "marque_styled",
        "prix_styled",
        "prix_remise_styled",
        "stock_styled",
        "show_on_home",
        "home_order",
        "active",
    )

    list_display_links = (
        "image_tag",
        "nom_styled",
    )

    list_editable = (
        "show_on_home",
        "home_order",
        "active",
    )

    list_filter = (
        "active",
        "show_on_home",
        "categorie",
        "sous_categorie",
        "marque",
    )

    search_fields = (
        "nom",
        "description",
        "slug",
        "categorie__nom",
        "sous_categorie__nom",
        "marque__nom",
    )

    ordering = (
        "home_order",
        "-id",
    )

    list_per_page = 20

    readonly_fields = (
        "slug",
        "image_preview",
    )

    autocomplete_fields = (
        "categorie",
        "sous_categorie",
        "marque",
    )

    inlines = [
        ProductImageInline,
    ]

    fieldsets = (
        ("Informations principales", {
            "fields": (
                "nom",
                "slug",
                "description",
                "active",
            )
        }),
        ("Affichage page d'accueil", {
            "fields": (
                "show_on_home",
                "home_order",
            )
        }),
        ("Catégorisation", {
            "fields": (
                "categorie",
                "sous_categorie",
                "marque",
            )
        }),
        ("Prix et stock", {
            "fields": (
                "prix",
                "prix_remise",
                "stock",
            )
        }),
        ("Image principale", {
            "fields": (
                "image",
                "image_preview",
            )
        }),
    )

    @admin.display(description="Image")
    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:54px; height:54px; object-fit:cover; '
                'border-radius:10px; border:1px solid #ddd;" />',
                obj.image.url
            )

        return format_html('<span style="color:#999; font-size:12px;">Pas d’image</span>')

    @admin.display(description="Nom", ordering="nom")
    def nom_styled(self, obj):
        return format_html(
            '<span style="font-weight:700; color:#1f2d2a; font-size:14px;">{}</span>',
            obj.nom
        )

    @admin.display(description="Catégorie", ordering="categorie__nom")
    def categorie_styled(self, obj):
        if obj.categorie:
            return badge(obj.categorie.nom, "#0b7478")

        return format_html('<span style="color:#999;">-</span>')

    @admin.display(description="Sous-catégorie", ordering="sous_categorie__nom")
    def sous_categorie_styled(self, obj):
        if obj.sous_categorie:
            return badge(obj.sous_categorie.nom, "#3b82f6")

        return format_html('<span style="color:#999;">-</span>')

    @admin.display(description="Marque", ordering="marque__nom")
    def marque_styled(self, obj):
        if obj.marque:
            return badge(obj.marque.nom, "#f97316")

        return format_html('<span style="color:#999;">-</span>')

    @admin.display(description="Prix", ordering="prix")
    def prix_styled(self, obj):
        return format_html(
            '<span style="font-weight:700; color:#0f766e;">{} DH</span>',
            obj.prix
        )

    @admin.display(description="Prix remise", ordering="prix_remise")
    def prix_remise_styled(self, obj):
        if obj.prix_remise:
            return format_html(
                '<span style="font-weight:700; color:#16a34a;">{} DH</span>',
                obj.prix_remise
            )

        return format_html('<span style="color:#999;">Aucune</span>')

    @admin.display(description="Stock", ordering="stock")
    def stock_styled(self, obj):
        if obj.stock == 0:
            return badge("Rupture", "#dc2626", min_width="76px")

        if obj.stock <= 10:
            return badge(f"{obj.stock} faible", "#f59e0b", min_width="76px")

        return badge(str(obj.stock), "#16a34a", min_width="60px")

    @admin.display(description="Aperçu image")
    def image_preview(self, obj):
        return image_preview_html(obj.image, "220px")


# ============================================================
# OFFERS
# ============================================================

@admin.register(OffreSpeciale)
class OffreSpecialeAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "prix_total",
        "date_expiration",
        "status_badge",
    )

    search_fields = (
        "nom",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("nom",),
    }

    @admin.display(description="Statut")
    def status_badge(self, obj):
        if obj.est_active():
            return badge("Active", "#16a34a")

        return badge("Expirée", "#dc2626")


# ============================================================
# PROMOTIONS
# ============================================================

class PromotionItemInline(admin.TabularInline):
    model = PromotionItem
    extra = 1

    autocomplete_fields = (
        "product",
    )

    fields = (
        "product",
        "product_preview",
        "original_price",
        "promo_price",
        "discount_badge",
        "active",
    )

    readonly_fields = (
        "product_preview",
        "original_price",
        "discount_badge",
    )

    @admin.display(description="Image")
    def product_preview(self, obj):
        if obj.product and obj.product.image:
            return format_html(
                '<img src="{}" style="width:48px; height:48px; object-fit:cover; '
                'border-radius:10px; border:1px solid #ddd;" />',
                obj.product.image.url
            )

        return format_html('<span style="color:#999;">-</span>')

    @admin.display(description="Prix normal")
    def original_price(self, obj):
        if obj.product:
            return format_html(
                '<span style="font-weight:700; color:#0f766e; white-space:nowrap;">{} DH</span>',
                obj.product.prix
            )

        return "-"

    @admin.display(description="Réduction")
    def discount_badge(self, obj):
        if obj.product and obj.promo_price:
            return badge(f"-{obj.get_discount_percentage()}%", "#dc2626", min_width="60px")

        return format_html('<span style="color:#999;">-</span>')


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date_range",
        "items_count",
        "status_badge",
        "show_home",
    )

    list_filter = (
        "active",
        "show_home",
        "start_date",
        "end_date",
    )

    search_fields = (
        "title",
        "description",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        ("Informations promotion", {
            "fields": (
                "title",
                "slug",
                "description",
            )
        }),
        ("Période", {
            "fields": (
                "start_date",
                "end_date",
            )
        }),
        ("Affichage", {
            "fields": (
                "active",
                "show_home",
            )
        }),
        ("Date de création", {
            "fields": (
                "created_at",
            )
        }),
    )

    inlines = [
        PromotionItemInline,
    ]

    @admin.display(description="Période")
    def date_range(self, obj):
        return format_html(
            '<span style="white-space:nowrap;">{} → {}</span>',
            obj.start_date.strftime("%d/%m/%Y"),
            obj.end_date.strftime("%d/%m/%Y")
        )

    @admin.display(description="Produits")
    def items_count(self, obj):
        return obj.items.count()

    @admin.display(description="Statut")
    def status_badge(self, obj):
        if obj.is_active_now():
            return badge("Active", "#16a34a", min_width="70px")

        if not obj.active:
            return badge("Inactive", "#6b7280", min_width="70px")

        return badge("Expirée", "#dc2626", min_width="70px")


@admin.register(PromotionItem)
class PromotionItemAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "promotion",
        "original_price",
        "promo_price_styled",
        "discount_badge",
        "active",
    )

    list_filter = (
        "promotion",
        "active",
        "product__categorie",
        "product__marque",
    )

    search_fields = (
        "product__nom",
        "promotion__title",
        "product__marque__nom",
        "product__categorie__nom",
    )

    autocomplete_fields = (
        "promotion",
        "product",
    )

    @admin.display(description="Produit", ordering="product__nom")
    def product_name(self, obj):
        return obj.product.nom

    @admin.display(description="Prix normal")
    def original_price(self, obj):
        return format_html(
            '<span style="font-weight:700; color:#0f766e; white-space:nowrap;">{} DH</span>',
            obj.product.prix
        )

    @admin.display(description="Prix promo", ordering="promo_price")
    def promo_price_styled(self, obj):
        return format_html(
            '<span style="font-weight:800; color:#dc2626; white-space:nowrap;">{} DH</span>',
            obj.promo_price
        )

    @admin.display(description="Réduction")
    def discount_badge(self, obj):
        return badge(f"-{obj.get_discount_percentage()}%", "#dc2626", min_width="60px")


# ============================================================
# CARTS
# ============================================================

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "session_key",
        "created_at",
        "is_ordered",
        "items_count",
    )

    list_filter = (
        "is_ordered",
        "created_at",
    )

    search_fields = (
        "user__username",
        "session_key",
    )

    inlines = [
        CartItemInline,
    ]

    @admin.display(description="Articles")
    def items_count(self, obj):
        return obj.store_items.count()


# ============================================================
# ORDERS
# ============================================================

class CustomerOrderItemInline(admin.TabularInline):
    model = CustomerOrderItem
    extra = 0
    can_delete = False

    readonly_fields = (
        "product",
        "offre",
        "name",
        "quantity",
        "unit_price",
        "total_price",
    )

    fields = (
        "name",
        "quantity",
        "unit_price",
        "total_price",
        "product",
        "offre",
    )


def update_order_status(modeladmin, request, queryset, status_value, success_message):
    updated = 0
    errors = []

    for order in queryset:
        try:
            order.status = status_value
            order.save()
            updated += 1
        except Exception as e:
            errors.append(f"Commande #{order.id}: {e}")

    if updated:
        modeladmin.message_user(
            request,
            success_message.format(updated=updated),
            level=messages.SUCCESS
        )

    if errors:
        modeladmin.message_user(
            request,
            " | ".join(errors),
            level=messages.ERROR
        )


@admin.action(description="Marquer comme confirmée")
def make_confirmed(modeladmin, request, queryset):
    update_order_status(
        modeladmin,
        request,
        queryset,
        "confirmed",
        "{updated} commande(s) confirmée(s). Le stock a été mis à jour si nécessaire."
    )


@admin.action(description="Marquer comme en traitement")
def make_processing(modeladmin, request, queryset):
    update_order_status(
        modeladmin,
        request,
        queryset,
        "processing",
        "{updated} commande(s) marquée(s) en traitement."
    )


@admin.action(description="Marquer comme livrée")
def make_delivered(modeladmin, request, queryset):
    update_order_status(
        modeladmin,
        request,
        queryset,
        "delivered",
        "{updated} commande(s) marquée(s) livrée(s)."
    )


@admin.action(description="Marquer comme annulée")
def make_cancelled(modeladmin, request, queryset):
    update_order_status(
        modeladmin,
        request,
        queryset,
        "cancelled",
        "{updated} commande(s) annulée(s). Le stock a été restauré si nécessaire."
    )


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "phone",
        "items_count",
        "total_to_pay_styled",
        "status_badge",
        "stock_deducted_badge",
        "whatsapp_badge",
        "created_at",
    )

    list_display_links = (
        "id",
        "full_name",
    )

    list_filter = (
        "status",
        "stock_deducted",
        "sent_to_whatsapp",
        "created_at",
    )

    search_fields = (
        "id",
        "full_name",
        "phone",
        "email",
        "address",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    readonly_fields = (
        "user",
        "session_key",
        "full_name",
        "phone",
        "email",
        "address",
        "total_products",
        "shipping_cost",
        "total_to_pay",
        "stock_deducted",
        "sent_to_whatsapp",
        "receipt_preview",
        "receipt_image",
        "created_at",
    )

    fieldsets = (
        ("Informations client", {
            "fields": (
                "full_name",
                "phone",
                "email",
                "address",
                "user",
                "session_key",
            )
        }),
        ("Détails financiers et statut", {
            "fields": (
                "total_products",
                "shipping_cost",
                "total_to_pay",
                "status",
                "stock_deducted",
                "sent_to_whatsapp",
            )
        }),
        ("Bon de commande", {
            "fields": (
                "receipt_preview",
                "receipt_image",
            )
        }),
        ("Dates", {
            "fields": (
                "created_at",
            )
        }),
    )

    inlines = [
        CustomerOrderItemInline,
    ]

    actions = [
        make_confirmed,
        make_processing,
        make_delivered,
        make_cancelled,
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user").prefetch_related("items")

    @admin.display(description="Produits")
    def items_count(self, obj):
        return obj.items.count()

    @admin.display(description="Total", ordering="total_to_pay")
    def total_to_pay_styled(self, obj):
        return format_html(
            '<span style="font-weight:800; color:#0f766e; white-space:nowrap;">{} DH</span>',
            obj.total_to_pay
        )

    @admin.display(description="Aperçu du bon")
    def receipt_preview(self, obj):
        if obj.receipt_image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="max-width:260px; border-radius:12px; border:1px solid #ddd;" />'
                '</a>',
                obj.receipt_image.url,
                obj.receipt_image.url
            )

        return format_html('<span style="color:#999;">Aucune image</span>')

    @admin.display(description="Statut")
    def status_badge(self, obj):
        styles = {
            "new": ("Nouvelle", "#2563eb"),
            "confirmed": ("Confirmée", "#059669"),
            "processing": ("Traitement", "#d97706"),
            "delivered": ("Livrée", "#16a34a"),
            "cancelled": ("Annulée", "#dc2626"),
        }

        label, color = styles.get(obj.status, (obj.status, "#6b7280"))

        return badge(label, color, min_width="82px")

    @admin.display(description="Stock")
    def stock_deducted_badge(self, obj):
        if obj.stock_deducted:
            return badge("Déduit", "#16a34a", min_width="74px")

        return badge("Non déduit", "#6b7280", min_width="86px")

    @admin.display(description="WhatsApp")
    def whatsapp_badge(self, obj):
        if obj.sent_to_whatsapp:
            return badge("Oui", "#16a34a", min_width="52px")

        return badge("Non", "#dc2626", min_width="52px")


# ============================================================
# REVIEWS
# ============================================================

@admin.register(AvisClient)
class AvisClientAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "produit",
        "note_badge",
        "date_ajout",
    )

    list_filter = (
        "note",
        "date_ajout",
    )

    search_fields = (
        "user__username",
        "produit__nom",
        "commentaire",
    )

    @admin.display(description="Note")
    def note_badge(self, obj):
        return badge(f"{obj.note}/5", "#0b7478", min_width="56px")


# ============================================================
# ADMIN TITLES
# ============================================================

admin.site.site_header = "City Pharma Plus Administration"
admin.site.site_title = "City Pharma Plus Admin"
admin.site.index_title = "Gestion des produits, catégories et commandes"