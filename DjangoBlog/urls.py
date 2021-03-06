"""DjangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from accounts.views import (
    login_view,
    register_view,
    logout_view)
# from posts import views as post_view

from django_email_verification import urls as mail_urls


urlpatterns = [
    # path('admin/defender/', include('defender.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('email/', include(mail_urls)),
    path('comments/', include("comments.urls", namespace="comments")),
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('', include("posts.urls", namespace="posts")),
    # path('posts/<int:post_id>', "<appname>.views.<function_name>"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns