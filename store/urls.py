from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path("scanner-stock/", views.scanner_stock, name="scanner_stock"),
    path("stock-dashboard/", views.stock_dashboard, name="stock_dashboard"),
    path("stock/export-excel/", views.export_stock_excel, name="export_stock_excel"),
    path("stock/movements/", views.stock_movements, name="stock_movements"),

    # Cart
    path('cart/', views.cart, name='cart'),
    path('cart/delete/', views.delete_cart, name='delete_cart'),
    path('cart/send/', views.checkout, name='passe_order'),
    path('cart/remove/<int:item_id>/', views.remove_item, name='remove_item'),
    path('cart/update/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('cart/update-ajax/<int:item_id>/', views.update_quantity_ajax, name='update_quantity_ajax'),
    # Search
    path('search/', views.search_products, name='search_products'),

    # Checkout / Order
    path('checkout/', views.checkout, name='checkout'),
    path("order-success/", views.order_success, name="order_success"),

    # Products
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/add_to_cart/', views.add_to_cart, name='add_to_cart'),

    # Categories
    path('categorie/<slug:slug>/', views.produits_par_categorie, name='produits_par_categorie'),
    path('sous-categorie/<slug:slug>/', views.products_by_subcategory, name='products_by_subcategory'),

    # Marques
    path('marque/<str:marque_nom>/', views.produits_par_marque, name='produits_par_marque'),
    path('marques/', views.marques_grid, name='marques_grid'),
    path('marques/<int:marque_id>/', views.detail_marque, name='detail_marque'),
    path('marques-produits/', views.marques_et_produits, name='marques_et_produits'),
    

    # Pages
    path('qui-sommes-nous/', views.qui_sommes_nous, name='qui'),

    # Login
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # Offres
    path('offres/', views.liste_offres, name='liste_offres'),
    path('offres/<slug:slug>/', views.detail_offre, name='detail_offre'),
    path('offres/<slug:slug>/ajouter/', views.add_offer_to_cart, name='add_offer_to_cart'),
]
# from django.urls import path
# from . import views
# from .views import passe_order
# from .views import cart, index, product_detail, add_to_cart, delete_cart, passe_order
# from django.contrib.auth import views as auth_views


# app_name = 'offres'

# app_name = 'store'  # يفضل إضافة app_name لتسهيل العناوين العكسية (reverse)

# urlpatterns = [
    
#     path('', views.index, name='index'),  # صفحة عرض جميع المنتجات
#     path('cart/', views.cart, name='cart'),  # صفحة عربة التسوق
#     # paht('qui/',views.qui, name='qui'),
#     path('product/<slug:slug>/', views.product_detail, name='product_detail'),  # تفاصيل المنتج
#     path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),  # إضافة منتج للعربة
#     path('delete-cart/', views.delete_cart, name='delete_cart'),  # حذف عربة التسوق
#     path('order/', views.passe_order, name='passe_order'),  # تمرير الطلب (إرسال)
#     path('cart/', views.cart, name='cart'), 
    
#         # ✅ أضف هذا المسار لصفحة "Qui sommes-nous"
#     path('qui-sommes-nous/', views.qui_sommes_nous, name='qui'),
     
#     path('cart/delete/', views.delete_cart, name='delete_cart'),
#     path('cart/send/', views.passe_order, name='passe_order'),
    
    

#     path('product/<slug:slug>/', views.product_detail, name='product_detail'),
#     path('product/<slug:slug>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    
#     path('categorie/<str:nom_categorie>/', views.produits_par_categorie, name='produits_par_categorie'),
    
#     path('cart/delete/', views.delete_cart, name='delete_cart'),
#     path('cart/send/', views.passe_order, name='passe_order'),

#     path('product/<slug:slug>/add_to_cart/', views.add_to_cart, name='add_to_cart'),

#     path('categorie/<str:nom_categorie>/', views.produits_par_categorie, name='produits_par_categorie'),
    
#     path('marque/<str:marque_nom>/', views.produits_par_marque, name='produits_par_marque'),
    
#     path('marques/', views.marques_et_produits, name='marques_et_produits'),


#     path('marques/', views.marques_grid, name='marques_grid'),
#     # path('marque/<int:marque_id>/', views.produits_par_marque, name='produits_par_marque'),
#     path('marques/<int:marque_id>/', views.detail_marque, name='detail_marque'),

# path('marques-produits/', views.marques_et_produits, name='marques_et_produits'),
#     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
# #CARTE
# path('remove-item/<int:item_id>/', views.remove_item, name='remove_item'),

# # path('panier/ajouter/<int:offre_id>/', views.ajouter_offre_au_panier, name='ajouter_offre_au_panier'),

#     path('cart/', views.cart, name='cart'),
#     path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

#  path('', views.liste_offres, name='liste'),
#     path('<slug:slug>/', views.detail_offre, name='detail'),
#     path('<slug:slug>/ajouter/', views.add_offer_to_cart, name='add_offer_to_cart'),





# ]
