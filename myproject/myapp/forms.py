# forms.py
# forms.py
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'profile_picture', 'bio', 'location']  # Make sure to include all fields
