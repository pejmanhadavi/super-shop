from django.urls import path
from django.views.generic import TemplateView

from .views import ShopListView,ProductDetailView,CategoryList


urlpatterns = [
    path('', ShopListView.as_view(), name='index'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>', CategoryList.as_view(), name='category_list'),
]