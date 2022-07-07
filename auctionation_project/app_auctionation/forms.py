from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from .models import Comment


class UserCreateForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        ),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email'
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.filter(email=email):
            raise ValidationError("User with this email already exists.")

        if User.objects.filter(username=username):
            raise ValidationError("This username has already been taken. Please pick another one.")

        if password:
            if password != password2:
                raise ValidationError("Password must be same!")


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )


class UserResetPasswordForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )
    old_password = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Current password'
            }
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'New password'
            }
        ),
        validators=[validate_password],
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'New password'
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        old_password = cleaned_data.get('old_password')

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("User specified by given username does not exist.")

        user_authenticate = authenticate(
            username=username,
            password=old_password
        )

        if not user_authenticate:
            raise ValidationError(f"Invalid password for user {username}")

        password = cleaned_data.get('new_password')
        password2 = cleaned_data.get('new_password2')

        if password:
            if old_password == password:
                raise ValidationError("Old and new password must be different.")

            if password != password2:
                raise ValidationError("Passwords must be same.")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]