from django import forms
from django.utils.translation import gettext_lazy as _



from .models import Review

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('review',)