from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recommendation
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username (letters, digits, @/./+/-/_ only)'
        }),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password'
        }),
        help_text="Your password must contain at least 8 characters."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        help_text="Enter the same password as before, for verification."
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")
        
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    _user = None  # Stocker l'utilisateur après authentification

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user_model = get_user_model()
                user = user_model.objects.get(email=email)
                authenticated_user = authenticate(username=user.username, password=password)
                if authenticated_user is None:
                    raise ValidationError("Invalid email or password")
                self._user = authenticated_user
            except user_model.DoesNotExist:
                raise ValidationError("No user with this email was found")

        return self.cleaned_data

    def get_user(self):
        return self._user

    
    
class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address'
        }),
        max_length=254,
        required=True
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        }),
        strip=False,
        help_text="Your password must contain at least 8 characters."
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        }),
        strip=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")
        
        if password1 and len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        return cleaned_data

    def save(self, request=None):
        User = get_user_model()
        email = self.cleaned_data['email']
        new_password = self.cleaned_data['new_password1']
        
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return user
        except User.DoesNotExist:
            raise ValidationError("User with this email does not exist.")

class RecommendationForm(forms.Form):
    name = forms.CharField(
        label='Your/Company Name',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name or company name'
        })
    )
    
    activity_field = forms.ChoiceField(
        label='Industry/Activity Field',
        choices=Recommendation.ACTIVITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    storage_needs = forms.FloatField(
        label='Storage needs (in GB)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 500',
            'step': '0.1'
        })
    )
    
    supports_encryption = forms.TypedChoiceField(
        label='Supports encryption?',
        choices=[(1, 'Yes'), (0, 'No')],
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    cpu_speed = forms.FloatField(
        label='CPU speed (GHz)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 3.5',
            'step': '0.1'
        })
    )
    
    price_per_hour = forms.FloatField(
        label='Price per hour ($)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 2.5',
            'step': '0.01'
        })
    )
    
    service_model_score = forms.ChoiceField(
        label='Service model score (1-5)',
        choices=[(1, '1 - Low'), (2, '2'), (3, '3 - Medium'), 
                (4, '4'), (5, '5 - High')],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
