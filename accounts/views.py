from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import UserLoginForm, UserRegisterForm, UserPasswordChangeForm, UserPasswordResetForm
from .models import LaFrescoUser


def login_user(request):
    if request.user.is_authenticated:
        return redirect('cart:list_items')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('cart:list_items')
        elif not LaFrescoUser.objects.get(email=email).is_active:
            messages.error(request, 'Your account is not active. Please use forgot your password in login option to reset.')
        else:
            messages.error(request, 'Email or password is not correct.')
    return render(request, 'accounts/login.html', context={'form': form})


def confirm_register_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = LaFrescoUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, LaFrescoUser.DoesNotExist):
        user = None
    if user is not None:
        if default_token_generator.check_token(user=user, token=token):
            user.is_active = True
            user.save()
            context = {
                'registration_successful': True
            }
        else:
            messages.error(request, 'Invalid Token or Token expired. Please obtain a new token.')
            context = {
                'registration_successful': False
            }
    else:
        context = {
            'registration_successful': False
        }
    return render(request, 'accounts/confirm_register.html', context)


def register_user(request):
    form = UserRegisterForm(request.POST or None)
    temp_successful = False
    if form.is_valid():
        user = form.save()
        temp_successful = True
        subject = 'Confirm Registration for LaFresco'
        message = 'Someone asked for account registration for email {email}. Follow the link below:'.format(
            email=user.email)
        send_email_helper(user, subject, message, [user.email], 'confirm_registration')
    return render(request, 'accounts/register.html', {'form': form, 'successful': temp_successful})


def logout_user(request):
    logged_out = False
    if request.user.is_authenticated:
        logout(request)
        logged_out = True
    return render(request, 'accounts/logout.html', {'logged_out': logged_out})


def send_email_helper(user, subject, message, recipient, url_path):
    token = default_token_generator.make_token(user=user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    message = message + '\n{protocol}://{domain}/accounts/{url_path}/{uidb64}/{token}'. \
        format(protocol=settings.PROTOCOL, domain=settings.DOMAIN,
               email=user.email, uidb64=uidb64, token=token, url_path=url_path)
    send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
              recipient_list=recipient, fail_silently=False)


def password_reset(request):
    email = request.POST.get('email')
    mail_sent = False
    qs = LaFrescoUser.objects.filter(email=email)
    if qs.exists():
        subject = 'Password Reset for LaFresco'
        message = "You asked for a password reset for email {email}. Follow the link below:".format(email=email)
        send_email_helper(qs[0], subject, message, [email], 'password_reset_confirm')
        mail_sent = True
    return render(request, 'accounts/password_reset.html', {'mail_sent': mail_sent})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = LaFrescoUser.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, LaFrescoUser.DoesNotExist):
        user = None
    password_changed = False
    if user is not None:
        if default_token_generator.check_token(user=user, token=token):
            form = UserPasswordResetForm(request.POST or None)
            if form.is_valid():
                new_password = request.POST['new_password1']
                user.set_password(new_password)
                user.save()
                password_changed = True
            return render(request, 'accounts/password_reset_confirm..html',
                          {'form': form, 'password_changed': password_changed})
        else:
            messages.error(request, 'Invalid Token or Token expired. Please obtain a new token.')
    return render(request, 'accounts/password_reset_confirm..html', {'password_changed': password_changed})


@login_required
def password_change(request):
    form = UserPasswordChangeForm(request.POST or None)
    if form.is_valid():
        email = request.POST['email']
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        user = authenticate(email=email, password=current_password)
        if user is not None:
            user.set_password(new_password)
            user.save()
            return redirect('accounts:profile', user_id=user.id)
        messages.error(request, 'Email or Password is not correct. ')
    return render(request, 'accounts/change-password.html', {'form': form})


@login_required
def profile(request, user_id):
    user = LaFrescoUser.objects.get(id=user_id)
    if user is not None:
        if request.method == 'POST':
            first_name = request.POST.get('first_name' or None)
            last_name = request.POST.get('last_name' or None)
            date_of_birth = request.POST.get('date_of_birth' or None)
            if first_name and user.first_name != first_name:
                user.first_name = first_name
            if last_name and user.last_name != last_name:
                user.last_name = last_name
            if date_of_birth and user.date_of_birth != date_of_birth:
                user.date_of_birth = date_of_birth
            user.save()
    return render(request, 'accounts/user-profile.html', {'user': user})
