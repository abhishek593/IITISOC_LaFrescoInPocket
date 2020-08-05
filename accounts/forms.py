from django import forms
from .models import LaFrescoUser


class UserLoginForm(forms.Form):
    email = forms.CharField(label='Email Address', widget=forms.EmailInput(
        attrs={'class': 'form-control col-md-6',
               'placeholder': 'Enter your email',
               'aria-describedby': 'emailHelp'
               }
        ), required=True
    )
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control col-md-6',
               'placeholder': 'Enter Password'}
        ), required=True
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = LaFrescoUser.objects.filter(email=email)
        if qs.exists():
            return email
        raise forms.ValidationError('This email is not registered.')


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={
            'class': 'form-control col-md-6',
            'placeholder': 'First Name'}
        ), required=True
    )
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={
            'class': 'form-control col-md-6',
            'placeholder': 'Last Name'}
        ), required=True
    )
    date_of_birth = forms.DateField(label='Date-Of-Birth', widget=forms.DateInput(
        attrs={'class': 'form-control col-md-6',
               'placeholder': 'yyyy-mm-dd'}))
    email = forms.CharField(label='Email Address', widget=forms.EmailInput(
        attrs={'class': 'form-control col-md-6',
               'placeholder': 'Enter your email',
               'aria-describedby': 'emailHelp'
               }
        ), required=True
    )
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control col-md-6',
               'placeholder': 'Enter Password'}
        ), required=True
    )
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control col-md-6',
               'placeholder': 'Confirm Password'}
        ), required=True
    )

    class Meta:
        model = LaFrescoUser
        fields = ('email', 'date_of_birth', 'first_name', 'last_name')

    def clean_email(self):
        email_form_value = self.cleaned_data.get('email')
        user = LaFrescoUser.objects.get(email=email_form_value)
        if user.is_active:
            return email_form_value
        raise forms.ValidationError("""
            Your account is registered with us. 
            Please click on forgot your password to reset your password.
        """)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserPasswordChangeForm(forms.Form):
    email = forms.CharField(label='Email Address', widget=forms.EmailInput(
        attrs={'class': 'form-control col-md-6',
               'placeholder': 'Enter email',
               }
        ), required=True
    )
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control col-md-6',
               'placeholder': 'Current Password'}
        ), required=True
    )
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control col-md-6',
               'placeholder': 'New Password'}
        ), required=True
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = LaFrescoUser.objects.filter(email=email)
        if qs.exists():
            return email
        raise forms.ValidationError('This email is not registered.')


class UserPasswordResetForm(forms.Form):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control col-md-6',
               'placeholder': 'New Password'}
        ), required=True
    )
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control col-md-6',
               'placeholder': 'Confirm New Password'}
        ), required=True
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
