from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages


def contact(request):
        if request.method == 'POST':
          name = request.POST['name']
          email = request.POST['email']
          message = request.POST['message']
          contact = Contact.objects.create(name=name, email=email, message=message)
          contact.save()
          messages.success(request, 'OK thanks ill call you back soon :)) ')
          return redirect('contact')
        else:
          return render(request, 'pages/contact.html')
     