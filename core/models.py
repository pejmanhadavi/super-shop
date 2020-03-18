from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField(blank=True)
    def __str__(self):
       return self.name