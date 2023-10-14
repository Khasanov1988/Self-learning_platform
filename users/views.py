import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, UserLoginForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        # Send a welcome email to the user upon successful registration
        send_mail(
            subject='Congratulations on successful registration at Distribution App!',
            message='Welcome to our platform',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email],
        )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # Method works with success validation
        print(form.data.get('password1'))
        print(form.data.get('password2'))
        print(form.is_valid())
        if form.is_valid():
            self.object = form.save()
            if form.data.get('password1') == form.data.get('password2') and form.data.get('password1') != "":
                self.object.set_password(form.data.get('password1'))
            self.object.save()
        return super().form_valid(form)


class LoginModifiedView(LoginView):
    model = User
    form_class = UserLoginForm


def generate_new_password(request):
    # Generate a new random password
    characters = string.ascii_letters + string.digits + string.punctuation
    new_password = ''.join(random.choice(characters) for _ in range(12))
    # Send an email to the user with the new password
    send_mail(
        subject='You have changed your password on Distribution App',
        message=f'Your new password is: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
    )

    # Set the user's password to the new random password
    request.user.set_password(new_password)
    request.user.save()

    # Redirect the user to the home page
    return redirect(reverse('users:login'))
