from django.shortcuts import render
from django.views.generic import ListView, DetailView 

from .models import Category, Product


class ShopListView(ListView):
    model = Product
    queryset = Product.objects.order_by("-created_at")
    template_name = 'pages/index.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
