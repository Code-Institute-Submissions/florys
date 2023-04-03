from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('register/', views.UserRegisterView.as_view(), name='register'),
                  path('edit_profile/', views.UserEditView.as_view(), name='edit_profile'),
                  path('password/', views.PasswordsChangeView.as_view(template_name='registration/change_password.html')),
                  path('password_success', views.password_success, name='password_success'),
                  path('<int:pk>/profile/', views.ShowProfilePageView.as_view(), name='show_profile_page'),
                  path('<int:pk>/edit_profile_page/', views.EditProfilePageView.as_view(), name='edit_profile_page'),
                  path('create_profile_page/', views.CreateProfilePageView.as_view(), name='create_profile_page'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
