from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect, render
from .forms import * 
from user_profile.models import UserProfile
from django.core.mail import send_mail

def home(request):
    return render(request, 'account/home.html')

def aboutus(request):
    return render(request, 'account/aboutus.html')

def contact(request):
    if request.method == "GET":
        return render(request, 'account/contact.html')
    else:
        data = request.POST
        body = f"Email: - {data['email']} \n Name: - {data['name']} \n Subject: - {data['subject']} \n Body: - {data['message']}"
        send_mail(
            data['subject'],
            body,
            data['email'],
            ['manishjha5410@gmail.com'],
            fail_silently=False,
        )
        return render(request, 'account/contact.html',{'message' : data['name']})


def SignUp(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = user.first_name
            last_name = user.last_name
            name = first_name + ' ' + last_name
            UserProfile.objects.create(name=name, user=user)
            login(request, user)
            return redirect('account:home')
    else:
        form = UserCreateForm()
    return render(request, 'account/signup.html', {'form': form})