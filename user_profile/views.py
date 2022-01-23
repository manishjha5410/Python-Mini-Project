from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Create your views here.
@login_required(login_url='/login/')
def CreateUserProfile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            password = User.objects.make_random_password()
            username = profile.name.split()[0] + id_generator()
            user = User.objects.create(username=username, user_type="P")
            user.set_password(password)
            user.save_base(raw=True)
            profile.user = user
            profile.save()
            return redirect('appointment:r_dashboard')
    else:
        form = ProfileUpdateForm()
    return render(request, 'user_profile/profile_create.html', {'form': form})


@login_required(login_url='/login/')
def UpdatedUserProfile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        profile.name = request.POST['name']
        profile.phone = request.POST['phone']
        profile.email = request.POST['email']
        profile.gender = request.POST['gender']
        profile.age = request.POST['age']
        profile.address = request.POST['address']
        profile.blood_group = request.POST['blood_group']
        if 'med_reps' in request.FILES:
            profile.med_reps = request.FILES['med_reps']
        profile.case_paper = request.POST['case_paper']
        profile.save()
        return redirect('user_profile:profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'user_profile/profile.html', {'type':'user','form': form, 'dup':profile,'user':user})

@login_required(login_url='/login/')
def UpdatedDoctorProfile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        profile.name = request.POST['name']
        profile.phone = request.POST['phone']
        profile.email = request.POST['email']
        profile.gender = request.POST['gender']
        profile.age = request.POST['age']
        profile.address = request.POST['address']
        if 'med_reps' in request.FILES:
            profile.med_reps = request.FILES['med_reps']
        profile.salary = request.POST['salary']
        profile.attendance = request.POST['attendance']
        profile.status = request.POST['status']
        return redirect('user_profile:profile_d')
    else:
        form = DoctorProfileForm(instance=profile)
    return render(request, 'user_profile/profile_d.html', {'type':'doctor','form': form, 'dup':profile,'user':user})


@login_required(login_url='/login/')
def UpdatedUserProfilePk(request, pk):
    user = User.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('appointment:r_dashboard')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'user_profile/profile.html', {'form': form, 'user':user})


@login_required(login_url='/login/')
def UpdatedDocProfilePk(request, pk):
    user = User.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('appointment:hr_dashboard')
    else:
        form = DoctorProfileForm(instance=profile)
    return render(request, 'user_profile/profile.html', {'type':'doctor','form': form, 'dup':profile,'user':user})


@login_required(login_url='/login/')
def DeleteUserProfilePk(request, pk):
    user = User.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        user.delete()
        return redirect('appointment:r_dashboard')
    else:
        return render(request, 'user_profile/profile_delete.html', {'user':user})


@login_required(login_url='/login/')
def DeleteDocProfilePk(request, pk):
    print("hello")
    user = User.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        user.delete()
        return redirect('appointment:hr_dashboard')
    else:
        return render(request, 'user_profile/profile_doc_delete.html', {'user':user})