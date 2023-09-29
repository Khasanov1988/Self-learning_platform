import random

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
    success_url = reverse_lazy('education_content:list')

    def get_object(self, queryset=None):
        return self.request.user


class LoginModifiedView(LoginView):
    model = User
    form_class = UserLoginForm


def generate_new_password(request):
    # Generate a new random password
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])

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
    return redirect(reverse('distribution:home'))

