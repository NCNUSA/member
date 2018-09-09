"""member URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from backend import views

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('edit/<str:gp>/<str:sid>/', views.edit, name='edit'),
    path('edit/', views.edit, name='edit.save'),
    path('Group/', views.group_list, name='gp.list'),
    path('Group/<int:uid>', views.group_detail, name='gp.detail'),
    path('Group/edit/<str:gp>/', views.GPedit, name='gp.edit'),
    path('GoogleSheet/', views.googleSheet, name='GoogleSheet'),
    path('GoogleSheet/<int:UID>', views.googleSheet, name='GoogleSheet.detail'),
    path('accounts/', include('django.contrib.auth.urls')),
]
