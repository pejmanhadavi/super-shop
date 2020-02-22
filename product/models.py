from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(max_length=150, blank=False, null=False, verbose_name=_('slug'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', args=[str(self.slug)])
