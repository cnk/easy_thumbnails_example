from django import forms
from .models import UserProfile


class AvatarForm(forms.ModelForm):
    """
    Allows the user to upload an image that will be scaled to use as their avatar.
    """
    class Meta:
        model = UserProfile
        fields = ('avatar',)
