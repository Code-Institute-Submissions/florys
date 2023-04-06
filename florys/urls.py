from django.contrib import admin
from django.urls import path, include
from florys.views import InitialView

urlpatterns = [
    path('', InitialView.as_view(), name='home_page'),
    path('admin/', admin.site.urls),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('blog.urls'), name='blog_urls'),
]

