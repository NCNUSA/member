import xlrd
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, render

from utils import google_sheet_utils

from .forms import SheetCheckForm
from .models import *


@login_required
def index(request):
    """首頁，擁有搜尋會員功能"""
    if "Q" in request.GET:
        query = request.GET["Q"].strip()
        if len(query) == 0:
            return redirect(index)
        search_param = query.split()
        result = Member.objects.query_member(search_param)
        return render(request, "index.html", locals())
    else:
        return render(request, "index.html")


@login_required
def group_list(request):
    """群組清單，one of the nav bar item
    可以有：幹部群組、成員群組 等等
    """

    gp_list = Group.objects.group_list(request.user.id)

    return render(request, "Group/list.html", locals())


@login_required
def group_detail(request, uid):
    """群組詳細資料
    有每個人的身份：學號、姓名、職稱等等

    Args:
        request:
        uid: The user's group id
    """
    if UserPerms.objects.filter(user=request.user.id, gp=uid):
        edit = UserPerms.objects.get(user=request.user.id, gp=uid).edit
        gp = Group.objects.get(id=uid)
        gp_member = GroupMember.objects.filter(GP__id=uid)
        return render(request, "Group/detail.html", locals())
    else:
        raise PermissionDenied


@login_required
def group_member_update(request, gp=0, sid=0):
    """編輯群組成員的個人資料
    內容包括：職稱、電郵、電話
    注意：電話中的橫槓 - 都會被刪除

    Args:
        request:
        gp: Target user's Group ID
        sid: Target user's SID
    """
    if UserPerms.objects.filter(user=request.user.id, gp=gp, edit=True):
        if request.method == "GET":
            user = GroupMember.objects.get(GP__id=gp, MEMBER__SID=sid)
            return render(request, "Group/edit.html", locals())
        else:
            title = request.POST["title"].strip()
            email = request.POST["email"].strip()
            phone = request.POST["phone"].strip()
            GroupMember.objects.member_update(sid, gp, title, email, phone)
            return redirect(group_detail, gp)
    else:
        raise PermissionDenied


@login_required
def group_member_list_update(request, gp):
    """編輯群組成員名單

    Args:
        request:
        gp: Target group's id
    """
    if not UserPerms.objects.filter(user=request.user.id, gp=gp, edit=True):
        raise PermissionDenied

    if request.method == "POST":
        gp_id = request.POST["gp"].strip()
        add = request.POST["add"].strip().split(",")
        remove = request.POST["remove"].strip().split(",")
        gp = Group.objects.get(id=gp_id)
        GroupMember.objects.member_list_update(gp, add, remove)
        return redirect(group_detail, gp_id)
    return render(request, "Group/group_member_list_update.html", locals())


@login_required
def google_sheet(request, gid=0):
    """Google 表單資料, one of the nav bar item"""

    if gid != 0:
        try:
            sheet = GoogleSheet.objects.get(id=gid)
        except ObjectDoesNotExist:
            return HttpResponse("找不到該表單，請聯絡開發人員")
        table = google_sheet_utils.parse(sheet.URL, sheet.SID, sheet.CNAME, sheet.VIP)
        thead = table[0]
        tbody = table[1:]
        amount = len(tbody)
        SID, CNAME, VIP, EMAIL = sheet.SID, sheet.CNAME, sheet.VIP, sheet.EMAIL
        return render(request, "GoogleSheet/sheet.html", locals())

    else:
        gp = UserPerms.objects.filter(user=request.user.id)
        gp_list = [i.gp for i in gp]
        sheet = GoogleSheet.objects.filter(GP__in=gp_list)
        return render(request, "GoogleSheet/list.html", locals())


@login_required
def google_sheet_add(request):
    """新增 Google 表單的結果"""
    if request.method == "GET":
        gp = UserPerms.objects.filter(user=request.user.id)
        return render(request, "GoogleSheet/add.html", locals())

    elif request.method == "POST":
        if google_sheet_utils.add(request):
            return redirect(google_sheet)
        else:
            return HttpResponse("資料錯誤")


@login_required
def google_sheet_edit(request, uid):
    """編輯表單基本資料"""
    if request.method == "GET":
        gp = UserPerms.objects.filter(user=request.user.id)
        gs = GoogleSheet.objects.get(id=uid)
        return render(request, "GoogleSheet/edit.html", locals())

    elif request.method == "POST":
        if google_sheet_utils.edit(request):
            return redirect(google_sheet)
        else:
            return HttpResponse("資料錯誤")


@login_required
def sheet_check(request):
    """上傳 xls/xlsx，以檢查表單資料是否正確, one of the nav bar item"""
    if request.method == "POST":
        form = SheetCheckForm(request.POST, request.FILES)
        if form.is_valid():
            # read the data from form and calculate the value
            position = {
                "sid_pos": form.cleaned_data["sid"],
                "is_member__pos": form.cleaned_data["is_member"],
                "name_pos": form.cleaned_data["name"],
                "email_pos": form.cleaned_data["email"],
            }
            gid = form.cleaned_data["gid"]
            # read the data in memory directly
            input_excel = request.FILES["spreadsheet"].read()
            data = xlrd.open_workbook(file_contents=input_excel)
            result = []
            for table in data.sheets():
                # check the sheet
                tmp = Member.objects.sheet_check(gid, table, position)
                result.append(tmp)
            return render(request, "xls_check/result.html", locals())
        return render(request, "xls_check/upload.html", locals())
    # GET
    else:
        gp_list = Group.objects.group_list(request.user.id)
        form = SheetCheckForm()
    return render(request, "xls_check/upload.html", locals())
