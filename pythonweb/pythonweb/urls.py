"""pythonweb URL Configuration

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
from django.contrib import admin
from django.urls import path
from zktools import views
from zktools import toolsmain
from django.views.static import serve
from pythonweb import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'index/', views.index),
    path(r'zk_tools/', toolsmain.zk_tools),
    path(r'all_env/', toolsmain.all_env),
    path(r'get_flow_env/', toolsmain.get_all_flow_env),
    path(r'syn_env/', toolsmain.syn_commit),
    path(r'static/', serve, {"document_root": settings.STATICFILES_DIRS}),
]
