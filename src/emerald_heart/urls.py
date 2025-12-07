"""
URL configuration for emerald_heart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from __future__ import annotations

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView

from emerald_heart.sitemap import sitemap_data
from emerald_heart.views import EmeraldLogout
from emerald_heart.views.auth.login_form import EmeraldAuthForm

urlpatterns = [
    path(
        "robots.txt",
        cache_page(86_400)(TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),  # Cache 1 day
        name="robots-txt",
    ),
    path(
        "ai.txt",
        cache_page(86_400)(TemplateView.as_view(template_name="ai.txt", content_type="text/plain")),  # Cache 1 day
        name="ai-txt",
    ),
    path("sitemap.xml", sitemap, {"sitemaps": sitemap_data}, name="django.contrib.sitemaps.views.sitemap"),
    path(
        "auth/login/",
        auth_views.LoginView.as_view(
            template_name="login.html",
            extra_context={"hide_header_bar": True},
            authentication_form=EmeraldAuthForm,
        ),
        name="auth-login",
    ),
    path("auth/logout/", EmeraldLogout.as_view(), name="auth-logout"),
    path("admin/", admin.site.urls),
]
