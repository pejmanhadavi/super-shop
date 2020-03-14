from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import datetime
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(max_length=150, blank=False, null=False, verbose_name=_('slug'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        indexes = [
            models.Index(fields=['name', 'slug'], name='category_index'),
        ]
        ordering = ['name']        

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_list', args=[str(self.slug)])


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, blank=False, null=False, verbose_name=_('name'))
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, verbose_name=_('price'))
    description = models.TextField(blank=False, null=False, verbose_name=_('description'))
    photo = models.ImageField(upload_to='media/photos/', verbose_name=_('photo'))
    slug = models.SlugField(max_length=150, blank=False, null=False, verbose_name=_('slug'))
    created_at = models.DateTimeField(default=datetime.now, blank=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name=_('updated_at'))
    off = models.IntegerField(blank=True, null=True, default=0, verbose_name=_('off'))
    number = models.IntegerField( default=1, verbose_name=_('number'))
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='products', verbose_name=_('category'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('product', args=[str(self.slug)])       

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', args=[str(self.slug)])   

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', args=[str(self.slug)])  

class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank = False,
        null = False,
        verbose_name=_('product'))


    author = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        verbose_name=_('author'))

    review = models.TextField(
        max_length=512,
        blank=False,
        null=False,
        verbose_name=_('review'))

    created_at = models.DateTimeField(
        blank=False,
        null=False,
        auto_now_add=True,
        verbose_name=_('created at'))        

          
    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
        ordering = ['-created_at']

    def __str__(self):
        return self.review


class BasketItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    ordered = models.BooleanField(default=False)        
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    
    def get_total_item_price(self):
        return self.quantity * self.product.price


    def get_final_price(self):
        return self.get_total_item_price()
        

class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    products = models.ManyToManyField(BasketItem)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username    


    def get_total(self):
        total = 0
        for basket_item in self.products.all():
            total += basket_item.get_final_price()
        return total    

