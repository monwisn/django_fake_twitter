from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Book, Tweet


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
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, label='Password')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, label='Password Confirm')
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text='Optional. Format: DD-MM-YYYY', required=False, label='Birth Date')

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
        exclude = ("user",)
