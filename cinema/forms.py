from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile, WatchLater


class RegistrationForm(UserCreationForm):

    full_name = forms.CharField(
        max_length=200,
        label='ФИО',
        widget=forms.TextInput(attrs={
            'placeholder': 'ФИО'
        })
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email'
        })
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Логин'
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Логин'
        })

        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Пароль'
        })

        self.fields['password2'].label = 'Повторите пароль'
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Повторите пароль'
        })

        self.order_fields([
            'full_name',
            'email',
            'username',
            'password1',
            'password2'
        ])

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                'Пользователь с таким логином уже существует.'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже зарегистрирован.'
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        user.is_staff = False
        user.is_superuser = False
        user.is_active = True

        if commit:
            user.save()

            UserProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name']
            )

        return user


class LoginForm(forms.Form):

    login = forms.CharField(
        label='Логин или Email',
        widget=forms.TextInput(attrs={
            'placeholder': 'Логин или Email'
        })
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль'
        })
    )


class WatchLaterForm(forms.ModelForm):

    class Meta:
        model = WatchLater

        fields = [
            'status',
            'rating'
        ]

        labels = {
            'status': 'Статус просмотра',
            'rating': 'Моя оценка'
        }

        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 10,
                'placeholder': 'От 1 до 10'
            })
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')

        if rating is not None and not 1 <= rating <= 10:
            raise forms.ValidationError(
                'Оценка должна быть от 1 до 10.'
            )

        return rating