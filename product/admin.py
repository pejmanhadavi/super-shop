from django.contrib import admin

from .models import Product, Category, BasketItem, Basket

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)    


admin.site.register(Product, ProductAdmin)    
admin.site.register(Category, CategoryAdmin)  
admin.site.register(Basket)  
admin.site.register(BasketItem)  
