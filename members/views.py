from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DetailView, CreateView, TemplateView
from .forms import SignUpForm, EditProfileForm, ChangePasswordForm, ProfilePageForm
from blog.models import Profile
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in


# Create your views here.
class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully, now please log in!.')
        return super().form_valid(form)


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('blog_home')

    def form_valid(self, form):
        messages.success(self.request, 'Settings updated!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('password_success')

    def form_valid(self, form):
        messages.success(self.request, 'Password Updated!')
        return super().form_valid(form)


def password_success(request):
    return render(request, 'registration/password_success.html', {})


class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'registration/create_user_profile_page.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Profile page created successfully!')
        return super().form_valid(form)


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context


class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url']

    success_url = reverse_lazy('blog_home')

    def form_valid(self, form):
        messages.success(self.request, 'Profile page edited successfully!')
        return super().form_valid(form)


class AccountLogout(TemplateView):
    template_name = 'registration/logout.html'


def handle_login(sender, request, **kwargs):
    messages.success(request, 'Welcome to Florys!')


user_logged_in.connect(handle_login)

