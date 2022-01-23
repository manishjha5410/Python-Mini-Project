from django.contrib.auth import get_user_model
from django import forms
from .models import *

class ProfileUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False, widget=forms.RadioSelect)
    class Meta:
        model = UserProfile
        fields = ('name', 'phone', 'email', 'gender', 'age', 'address', 'blood_group', 'med_reps', 'case_paper')


class DoctorProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False, widget=forms.RadioSelect)
    class Meta:
        model = UserProfile
        fields = ('name', 'phone', 'email', 'gender', 'age', 'address', 'department', 'attendance','med_reps', 'salary', 'status')