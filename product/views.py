from django.shortcuts import render
from django.views.generic import ListView, DetailView 

from .models import Category, Product


class ShopListView(ListView):
    model = Product
    queryset = Product.objects.order_by("-created_at")
    template_name = 'pages/index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ShopListView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['categories'] = Category.objects.order_by('name')  
        return context  


class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['categories'] = Category.objects.order_by('name')  
        return context  


class CategoryList(ListView):
    model = Category
    template_name = 'pages/index.html'
    context_object_name = 'categories'
    queryset = Category.objects.order_by('name')  

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CategoryList, self).get_context_data(**kwargs)
        # Add in the publisher
        context['categories'] = Category.objects.order_by('name')  
        return context  
