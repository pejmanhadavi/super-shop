from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView, View)  
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .models import (Category, Product, Review, BasketItem, Basket)

from .forms import ReviewForm


class ShopListView(ListView):
    model = Product
    queryset = Product.objects.order_by("-created_at")
    template_name = 'pages/index.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(ShopListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('name')  
        return context  


class BasketItemsView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            basket = Basket.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': basket,
                'categories' : Category.objects.order_by('name')  
            }
            return render(self.request, 'pages/basket_items.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have active basket :( ')
            return redirect('/')            
  


class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = 'pages/product_detail.html'
    form_class = ReviewForm
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']        
        context.update({
            'categories': Category.objects.order_by('name'),
            'review_list': Review.objects.filter(product = self.object.id),
            'review_form': ReviewForm(initial={'product': self.object.id })
        })        
        return context

    def get_success_url(self):
        return reverse('product_detail', kwargs={'slug': self.object.slug})
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        review = Review()
        review.product = self.object
        review.author = self.request.user.username
        review.review = form.cleaned_data['review']
        review.save()
        messages.success(self.request, _('Your review submited successfuly!'))
        return super(ProductDetailView, self).form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, _('failed.'))
        return super(ProductDetailView, self,).form_invalid(form)

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



class SearchResultsListView(ListView): 
    model = Product 
    context_object_name = 'products' 
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('name')  
        return context  

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(name__icontains=query)
        )


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    basket_item, created = BasketItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    basket_qs = Basket.objects.filter(user = request.user, ordered=False) #qs = queryset
    if basket_qs.exists():
        basket = basket_qs[0]
        # Check if the basket item is in the basket
        if basket.products.filter(product__slug=product.slug).exists():
            basket_item.quantity += 1
            basket_item.save()
            messages.info(request, 'this item quantity was updated !')
            return redirect('product_detail', slug=slug)    
        else:
            basket.products.add(basket_item)
            messages.info(request, 'This item was added to your cart :)')
            return redirect('product_detail', slug=slug)   
             
    else:
        basket = Basket.objects.create(user=request.user)
        basket.products.add(basket_item)
        messages.info(request, 'This item was added to your cart :)')
        return redirect('product_detail', slug=slug)    


@login_required
def add_single_item_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    basket_item, created = BasketItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    basket_qs = Basket.objects.filter(user = request.user, ordered=False) #qs = queryset
    if basket_qs.exists():
        basket = basket_qs[0]
        # Check if the basket item is in the basket
        if basket.products.filter(product__slug=product.slug).exists():
            basket_item.quantity += 1
            basket_item.save()
            messages.info(request, 'this item quantity was updated !')
            return redirect('basket-items')    
        else:
            basket.products.add(basket_item)
            messages.info(request, 'This item was added to your cart :)')
            return redirect('basket-items')   
             
    else:
        basket = Basket.objects.create(user=request.user)
        basket.products.add(basket_item)
        messages.info(request, 'This item was added to your cart :)')
        return redirect('basket-items')    



@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    basket_qs = Basket.objects.filter(
        user=request.user,
        ordered = False
    )
    if basket_qs.exists():
        basket = basket_qs[0]
        # Check if the basket item is in the basket
        if basket.products.filter(product__slug=product.slug).exists():
            basket_item = BasketItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            basket.products.remove(basket_item)
            messages.info(request, 'This item was removed from your cart :(')
            return redirect('basket-items') 
        else:
            messages.info(request, 'This item was not in your cart !')
            return redirect('product_detail', slug=slug)    
    else:
        messages.info(request, 'You do not have an active order !')
        return redirect('product_detail', slug=slug)
               


@login_required
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    basket_qs = Basket.objects.filter(
        user=request.user,
        ordered = False
    )
    if basket_qs.exists():
        basket = basket_qs[0]
        # Check if the basket item is in the basket
        if basket.products.filter(product__slug=product.slug).exists():
            basket_item = BasketItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if basket_item.quantity > 1 :
                basket_item.quantity -= 1
                basket_item.save()
            else:
                basket.products.remove(basket_item) 
            messages.info(request, 'This quantity was updated !')
            return redirect('basket-items') 
        else:
            messages.info(request, 'This item was not in your cart !')
            return redirect('product_detail', slug=slug)    
    else:
        messages.info(request, 'You do not have an active order !')
        return redirect('product_detail', slug=slug)
               