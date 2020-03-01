from django.urls import path
from django.views.generic import TemplateView

from .views import ShopListView,ProductDetailView


urlpatterns = [
    path('', ShopListView.as_view(), name='index'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
]