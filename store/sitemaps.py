from django.contrib.sitemaps import Sitemap
from .models import Product, Categorie, SousCategorie


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.filter(active=True)

    def location(self, obj):
        return f"/store/product/{obj.slug}/"


class CategorieSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Categorie.objects.all()

    def location(self, obj):
        return f"/store/categorie/{obj.slug}/"


class SousCategorieSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return SousCategorie.objects.all()

    def location(self, obj):
        return f"/store/sous-categorie/{obj.slug}/"


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return ["/store/"]

    def location(self, item):
        return item