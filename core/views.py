from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from product.models import Category, Product
from django.views.generic import (ListView, DetailView, View) 


def contact(request):
        if request.method == 'POST':
          name = request.POST['name']
          email = request.POST['email']
          message = request.POST['message']
          contact = Contact.objects.create(name=name, email=email, message=message)
          contact.save()
          messages.success(request, 'OK thanks ill call you back soon :)) ')
          context = {
                'categories' : Category.objects.order_by('name')  
            }          
          return render(request, 'pages/contact.html', context)
        else:
          context = {
                'categories' : Category.objects.order_by('name')  
            }               
          return render(request, 'pages/contact.html', context)
     

class CategoryList(ListView):
    model = Product
    template_name = 'pages/index.html'
    context_object_name = 'products'
    queryset = Category.objects.order_by('name') 

     
    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('name')  
        return context  


    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all()
        slug = self.kwargs['slug']
        if slug:
            category = Category.objects.filter(slug=slug).first()
            queryset = queryset.filter(category=category.id)
        return queryset         