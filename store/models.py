from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from marque.models import Marque


def unique_slugify(instance, value, slug_field_name='slug'):
    slug = slugify(value)
    model = instance.__class__
    unique_slug = slug
    num = 1

    while model.objects.filter(**{slug_field_name: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug}-{num}"
        num += 1

    return unique_slug


class Categorie(models.Model):
    nom = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.nom)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class SousCategorie(models.Model):
    parent = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    nom = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='sous_categories/', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = "Sous-catégorie"
        verbose_name_plural = "Sous-catégories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.nom)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:products_by_subcategory', args=[self.slug])

    def __str__(self):
        return f"{self.parent.nom} > {self.nom}"


class Product(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()

    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_remise = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    barcode = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Code-barres"
    )

    prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Prix d'achat"
    )

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    sous_categorie = models.ForeignKey(
        SousCategorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    stock = models.PositiveIntegerField(default=0)

    stock_min = models.PositiveIntegerField(
        default=2,
        verbose_name="Stock minimum"
    )

    image = models.ImageField(upload_to='products_img/', blank=True, null=True)

    marque = models.ForeignKey(
        Marque,
        on_delete=models.CASCADE,
        related_name='products'
    )

    slug = models.SlugField(unique=True, blank=True)
    active = models.BooleanField(default=True)
    show_on_home = models.BooleanField(default=False)
    home_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-id']
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def clean(self):
        super().clean()

        # تنظيف barcode قبل validation
        if self.barcode:
            self.barcode = self.barcode.strip()
        else:
            self.barcode = None

        if self.sous_categorie and self.categorie:
            if self.sous_categorie.parent_id != self.categorie_id:
                raise ValidationError({
                    'sous_categorie': "Cette sous-catégorie n'appartient pas à la catégorie sélectionnée."
                })

    def get_active_promotion_item(self):
        now = timezone.now()

        return (
            self.promotion_items
            .filter(
                active=True,
                promotion__active=True,
                promotion__start_date__lte=now,
                promotion__end_date__gte=now,
            )
            .order_by("promo_price")
            .first()
        )

    def get_price(self):
        promo_item = self.get_active_promotion_item()

        if promo_item:
            return promo_item.promo_price

        if self.prix_remise:
            return self.prix_remise

        return self.prix

    def get_old_price(self):
        """
        يرجع الثمن الأصلي إذا كان هناك تخفيض.
        نستعمله في الواجهة لعرض السعر مشطوب.
        """
        if self.get_active_promotion_item():
            return self.prix

        if self.prix_remise:
            return self.prix

        return None

    def has_active_promotion(self):
        return self.get_active_promotion_item() is not None

    def has_discount(self):
        return self.get_old_price() is not None

    def get_discount_percentage(self):
        promo_item = self.get_active_promotion_item()

        if promo_item:
            return promo_item.get_discount_percentage()

        if self.prix_remise and self.prix:
            discount = ((self.prix - self.prix_remise) / self.prix) * 100
            return round(discount)

        return 0

    def valeur_stock_achat(self):
        return self.prix_achat * self.stock

    def valeur_stock_vente(self):
        return self.get_price() * self.stock

    def benefice_potentiel(self):
        return self.valeur_stock_vente() - self.valeur_stock_achat()

    def is_low_stock(self):
        return self.stock <= self.stock_min

    def save(self, *args, **kwargs):
        # تنظيف barcode قبل الحفظ
        if self.barcode:
            self.barcode = self.barcode.strip()
        else:
            self.barcode = None

        if not self.slug:
            self.slug = unique_slugify(self, self.nom)

        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ("add", "Ajout au stock"),
        ("remove", "Retrait du stock"),
        ("adjust", "Ajustement"),
        ("sale", "Vente"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_movements"
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPES
    )

    quantity = models.PositiveIntegerField(default=1)

    old_stock = models.PositiveIntegerField(default=0)
    new_stock = models.PositiveIntegerField(default=0)

    note = models.CharField(max_length=255, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"

    def __str__(self):
        return f"{self.product.nom} - {self.get_movement_type_display()} - {self.quantity}"

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products_img/details/')
    alt_text = models.CharField(max_length=120, blank=True)

    class Meta:
        verbose_name = "Image produit"
        verbose_name_plural = "Images produits"

    def __str__(self):
        return f"Image for {self.product.nom}"


class OffreSpeciale(models.Model):
    nom = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='offres/', blank=True, null=True)
    date_expiration = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Offre spéciale"
        verbose_name_plural = "Offres spéciales"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.nom)

        super().save(*args, **kwargs)

    def est_active(self):
        return self.date_expiration is None or self.date_expiration > timezone.now()

    def __str__(self):
        return self.nom


class Promotion(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    active = models.BooleanField(default=True)
    show_home = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)

        super().save(*args, **kwargs)

    def is_active_now(self):
        now = timezone.now()
        return self.active and self.start_date <= now <= self.end_date

    def __str__(self):
        return self.title


class PromotionItem(models.Model):
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='promotion_items'
    )

    promo_price = models.DecimalField(max_digits=10, decimal_places=2)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produit en promotion"
        verbose_name_plural = "Produits en promotion"
        unique_together = ('promotion', 'product')

    def clean(self):
        if self.promo_price <= 0:
            raise ValidationError("Le prix promotionnel doit être supérieur à 0.")

        if self.product and self.promo_price >= self.product.prix:
            raise ValidationError(
                "Le prix promotionnel doit être inférieur au prix normal du produit."
            )

    def get_discount_percentage(self):
        if not self.product or not self.product.prix:
            return 0

        discount = ((self.product.prix - self.promo_price) / self.product.prix) * 100
        return round(discount)

    def get_price(self):
        if self.promotion.is_active_now() and self.active:
            return self.promo_price

        return self.product.get_price()

    def __str__(self):
        return f"{self.product.nom} - {self.promo_price} DH"


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.username} - Ordered: {self.is_ordered}"

        return f"Guest Cart {self.session_key} - Ordered: {self.is_ordered}"

    @property
    def total_price(self):
        return sum(item.get_price() for item in self.store_items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='store_items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    offre = models.ForeignKey(
        OffreSpeciale,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Article panier"
        verbose_name_plural = "Articles panier"

    def get_unit_price(self):
        if self.product:
            return self.product.get_price()

        if self.offre:
            return self.offre.prix_total

        return Decimal('0.00')

    def get_price(self):
        return self.get_unit_price() * self.quantity

    def __str__(self):
        if self.product:
            return f"{self.quantity} x {self.product.nom}"

        if self.offre:
            return f"{self.quantity} x {self.offre.nom}"

        return "CartItem"


class CustomerOrder(models.Model):
    STATUS_CHOICES = [
        ('new', 'Nouvelle commande'),
        ('confirmed', 'Confirmée'),
        ('processing', 'En traitement'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()

    total_products = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_to_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # هذا يمنع إنقاص stock مرتين
    stock_deducted = models.BooleanField(default=False, editable=False)

    sent_to_whatsapp = models.BooleanField(default=False)
    receipt_image = models.ImageField(
        upload_to='orders/receipts/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Commande client"
        verbose_name_plural = "Commandes clients"

    def __str__(self):
        return f"Commande #{self.id} - {self.full_name} - {self.total_to_pay} DH"

    def _check_stock_available(self):
        for item in self.items.select_related("product").all():
            if item.product and item.quantity > item.product.stock:
                raise ValidationError(
                    f"Stock insuffisant pour {item.product.nom}. "
                    f"Demandé: {item.quantity}, disponible: {item.product.stock}"
                )

    def _deduct_stock(self):
        for item in self.items.select_related("product").all():
            if item.product:
                product = item.product
                product.stock = max(product.stock - item.quantity, 0)
                product.save(update_fields=["stock"])

        self.stock_deducted = True
        CustomerOrder.objects.filter(pk=self.pk).update(stock_deducted=True)

    def _restore_stock(self):
        for item in self.items.select_related("product").all():
            if item.product:
                product = item.product
                product.stock += item.quantity
                product.save(update_fields=["stock"])

        self.stock_deducted = False
        CustomerOrder.objects.filter(pk=self.pk).update(stock_deducted=False)

    def clean(self):
        super().clean()

        if self.pk and self.status == "confirmed" and not self.stock_deducted:
            self._check_stock_available()

    def save(self, *args, **kwargs):
        old_stock_deducted = False

        if self.pk:
            old_order = CustomerOrder.objects.filter(pk=self.pk).only("stock_deducted").first()
            if old_order:
                old_stock_deducted = old_order.stock_deducted

        should_deduct_stock = (
            self.pk is not None
            and self.status == "confirmed"
            and not old_stock_deducted
        )

        should_restore_stock = (
            self.pk is not None
            and self.status == "cancelled"
            and old_stock_deducted
        )

        if should_deduct_stock:
            self._check_stock_available()

        super().save(*args, **kwargs)

        if should_deduct_stock:
            self._deduct_stock()

        elif should_restore_stock:
            self._restore_stock()


class CustomerOrderItem(models.Model):
    order = models.ForeignKey(
        CustomerOrder,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    offre = models.ForeignKey(
        OffreSpeciale,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Article commande"
        verbose_name_plural = "Articles commande"

    def __str__(self):
        return f"{self.quantity} x {self.name}"


class AvisClient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produit = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='avis')
    commentaire = models.TextField()
    note = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_ajout']
        verbose_name = "Avis client"
        verbose_name_plural = "Avis clients"

    def __str__(self):
        return f"Avis de {self.user} sur {self.produit.nom}"