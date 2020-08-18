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

There’s no need to add a leading slash, because every URL has that. For example,
 it’s articles, not /articles.
"""
from django.contrib import admin
from django.urls import include, path

from backend import views

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="home"),
    # 群組相關
    path(
        "Group/",
        include(
            [
                path("", views.group_list, name="gp.list"),
                path("<int:uid>", views.group_detail, name="gp.detail"),
                path(
                    "update/",
                    include(
                        [
                            path(
                                "<str:gp>/<str:sid>/",
                                views.group_member_update,
                                name="gp.update.member",
                            ),
                            path(
                                "<str:gp>/", views.group_member_list_update, name="gp.update.list"
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    # 連結到 Google 表單爬蟲後做檢查
    path(
        "GoogleSheet/",
        include(
            [
                path("", views.google_sheet, name="GoogleSheet"),
                path("create", views.google_sheet_add, name="GoogleSheet.add"),
                path("<int:gid>", views.google_sheet, name="GoogleSheet.detail"),
                path("update/<int:uid>", views.google_sheet_edit, name="GoogleSheet.update"),
            ]
        ),
    ),
    # 使用者上傳試算表格式，再做檢查
    path("SpreadsheetCheck", views.sheet_check, name="SpreadsheetCheck"),
    # 帳戶相關，重設密碼等等
    path("accounts/", include("django.contrib.auth.urls")),
    # LINE Bot 可用來查詢會員資料
    path("bot/", include("line_bot.urls")),
]
