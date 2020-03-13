from django.urls import path
from django.views.generic import TemplateView

from .views import (
ShopListView, 
ProductDetailView, 
CategoryList, 
SearchResultsListView,
BasketItemsView,
add_to_cart,
remove_from_cart,
remove_single_item_from_cart,
add_single_item_to_cart,
)  


urlpatterns = [
    path('', ShopListView.as_view(), name='index'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>', CategoryList.as_view(), name='category_list'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('basket-items/', BasketItemsView.as_view(), name='basket-items'),
    path('add-to-cart/<slug:slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:slug>', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug:slug>', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('add-item-to-cart/<slug:slug>', add_single_item_to_cart, name='add-single-item-to-cart'),
]