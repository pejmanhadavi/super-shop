from django.urls import path
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse

from . import views


def index(request):
    return redirect(reverse('index'))


urlpatterns = [
    path('', index),
    path('contact/', views.contact, name='contact'),
]
