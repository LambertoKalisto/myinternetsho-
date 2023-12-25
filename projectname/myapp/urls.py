from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import Search

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('search/', Search.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
