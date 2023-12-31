from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import Search, cart_add, cart_remove, CategorySearch

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('search/', Search.as_view(), name='search'),
    path('category-search/', CategorySearch.as_view(), name='category-search'),
    path('cart', views.cart, name='cart'),
    path('/add/<int:product_id>', cart_add, name='cart_add'),
    path('/remove/<int:product_id>', cart_remove, name='cart_remove'),
    path('cart/order', views.order, name='order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
