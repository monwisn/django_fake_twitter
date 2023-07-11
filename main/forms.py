from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetCompleteView

from .models import Book, Tweet, Profile


class AddForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'genre', 'author', 'isbn')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), required=False, help_text='Optional')
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30, required=True)
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}), max_length=100, required=True)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, label='Password:')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, label='Password Confirmation:')
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text='<small class="text-muted"><em>Use following format: DD-MM-YYYY  (Optional)</em></small>', required=False,
        label='Date of Birth:')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'birth_date']
        # widgets = {
        #     'password': forms.PasswordInput(),
        # }


class TweetForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder": "Enter Your Tweet here...",
                                   "class": "form-control",
                               }
                           ),
                           label="",
                           )

    class Meta:
        model = Tweet
        exclude = ("user", "likes")


class ClearableFileInputCustom(forms.ClearableFileInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['is_initial'] = False

        return context


class ProfileUpdateForm(forms.ModelForm):
    # profile_image = forms.ImageField(label='Profile Picture')

    class Meta:
        model = Profile
        fields = ('profile_image', 'profile_bio', 'homepage_link', 'instagram_link', 'linkedin_link')
        labels = {
            'profile_image': 'Profile Picture',
            'profile_bio': 'Profile Bio',
            'homepage_link': ' ',
            'instagram_link': ' ',
            'linkedin_link': ' ',
        }
        widgets = {
            'profile_image': ClearableFileInputCustom(attrs={'multiple': False}),
            'profile_bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Profile Bio'}),
            'homepage_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website Link'}),
            'instagram_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instagram Link'}),
            'linkedin_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Linkedin Link'}),

        }


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


