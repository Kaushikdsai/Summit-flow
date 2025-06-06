"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('login/register/',views.register,name='register'),
    path('timer/',views.timer,name='timer'),
    path('session/', views.session, name='session'),
    path('login/forgot-password/',views.forgotPassword,name='forgot-password'),
    path('password-reset-mail-sent/<str:reset_id>',views.mailSent,name='mail-sent'),
    path('reset-done/',views.resetDone,name='reset-done'),
    path('reset/<str:reset_id>/',views.newPassword,name='new-password'),
    path('bike1/',views.bike,name='bike'),
    path('update-metrics/',views.update_metrics,name='update-metrics'),
    path('user-dashboard/',views.user_dashboard,name='dashboard')
]