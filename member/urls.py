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
from django.conf.urls import url
from backend import views

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('edit/<str:gp>/<str:sid>/', views.group_member_update, name='edit'),
    path('Group/', views.group_list, name='gp.list'),
    path('Group/<int:uid>', views.group_detail, name='gp.detail'),
    path('Group/edit/<str:gp>/', views.group_member_list_update, name='gp.edit'),
    path('GoogleSheet/', views.google_sheet, name='GoogleSheet'),
    path('GoogleSheet/new', views.google_sheet_add, name='GoogleSheet.add'),
    path('GoogleSheet/<int:gid>', views.google_sheet, name='GoogleSheet.detail'),
    path('GoogleSheet/edit/<int:UID>', views.google_sheet_edit, name='GoogleSheet.edit'),
    path('sheet_check', views.sheet_check, name='sheet_check'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^bot/', include('line_bot.urls')),
]
