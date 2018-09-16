from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
from django.http import HttpResponse
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required


def Qfunction(query):
    """類 Google 搜尋，採用 AND"""
    QQuery = None
    for i in query:
        if QQuery == None:
            QQuery = Q(Q(SID__contains=i) | Q(GRADE__contains=i) | Q(DEP__contains=i) | Q(CNAME__contains=i))
        else:
            QQuery &= Q(Q(SID__contains=i) | Q(GRADE__contains=i) | Q(DEP__contains=i) | Q(CNAME__contains=i))
    return QQuery


@login_required
def index(request):
    if 'Q' in request.GET:
        query = request.GET['Q'].strip().split()
        result = Member.objects.filter( Qfunction(query) )
        return render(request, 'index.html', locals())
    else:
        return render(request, 'index.html')


@login_required
def group_list(request):
    gp_list = []
    for item in UserPerms.objects.filter(user = request.user.id):
        gp_list.append(item.gp)
    # print(gp_list)
    # gp_list = GP.objects.all()
    return render(request, 'Group/list.html', locals())


@login_required
def group_detail(request, uid):
    if UserPerms.objects.filter(user = request.user.id, gp = uid):
        edit = UserPerms.objects.get(user = request.user.id, gp = uid).edit
        gp = GP.objects.get(id=uid)
        gp_member = GPM.objects.filter(GP__id=uid)
        return render(request, 'Group/detail.html', locals())
    else:
        return HttpResponse("無此權限")


@login_required
def edit(request, gp=0, sid=0):
    """編輯群組成員的職稱"""
    if UserPerms.objects.filter(user = request.user.id, gp = gp, edit = True):
        if request.method == "GET":
            user = GPM.objects.get(GP__id=gp, MEMBER__SID=sid)
            return render(request, 'Group/edit.html', locals())
        else:
            title = request.POST['title'].strip()
            email = request.POST['email'].strip()
            phone = request.POST['phone'].strip()
            user = GPM.objects.get(GP__id=gp, MEMBER__SID=sid)
            user.TITLE = title
            user.save()
            m = user.MEMBER
            # 驗證 email 正確性
            try:
                validate_email(email)
                m.EMAIL = email
                m.save()
            except:
                if email == "":
                    m.EMAIL = None
                    m.save()
                pass
            if phone == "":
                m.PHONE = None
                m.save()
            else:
                m.PHONE = phone.replace('-', '')
                m.save()
            return redirect(group_detail, gp)
    else:
        return HttpResponse("無此權限")

@login_required
def GPedit(request, gp):
    """編輯群組成員"""
    if UserPerms.objects.filter(user = request.user.id, gp = gp, edit = True):
        if request.method == 'POST':
            gp_id = request.POST['gp'].strip()
            add = request.POST['add'].strip().split(',')
            remove = request.POST['remove'].strip().split(',')
            gp = GP.objects.get(id=gp_id)
            for i in add:
                sid = i.strip()
                if sid.strip() != '' and Member.objects.filter(SID=sid).exists() and not GPM.objects.filter(GP=gp, MEMBER__SID=sid).exists():
                    m = Member.objects.get(SID=sid)
                    GPM.objects.create(GP=gp, MEMBER=m)
            for i in remove:
                sid = i.strip()
                if sid.strip() != '' and Member.objects.filter(SID=sid).exists() and GPM.objects.filter(GP=gp, MEMBER__SID=sid).exists():
                    GPM.objects.filter(GP=gp, MEMBER__SID=sid).delete()
            return redirect(group_detail, gp_id)
        return render(request, 'Group/GPedit.html', locals())
    else:
        return HttpResponse("無此權限")
    


def parse_google_sheet(url, SID, CNAME, VIP):
    """爬蟲抓取該表單網頁，因為使用 js 生成網頁所以使用 Selenium"""
    from selenium import webdriver
    from bs4 import BeautifulSoup
    from selenium.webdriver import FirefoxOptions
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=opts)
    driver.get(url)
    bsObj = BeautifulSoup( driver.page_source, "html.parser" )
    rows = bsObj.find("table").find("tbody").find_all("tr")
    # 每列資料都塞在這裡面
    table = []
    for row in rows:
        columns = row.find_all("td")
        tmp_list = []
        for field in columns:
            tmp_list.append(field.text)
        table.append(tmp_list)
    # Google form 輸出結果第二行會是空白，將之移除
    try:
        table.remove([""]*len(table[0]))
    except:
        pass
    # 判斷姓名是否跟學號匹配
    if SID != None and CNAME != None:
        for index, row in enumerate(table):
            if index == 0:
                row.append("姓名是否匹配")
                continue
            try:
                m = Member.objects.get(SID=row[SID-1])
                if row[CNAME - 1] != m.CNAME:
                    row.append("錯誤(學生會資料庫：" + m.CNAME + ")")
                else:
                    row.append("")
            except:
                row.append("資料庫中尚未有此人")
    return table


@login_required
def googleSheet(request, UID=0):
    """Google 表單資料"""

    if UID != 0:
        try:
            sheet = GoogleSheet.objects.get(id=UID)
        except:
            return HttpResponse("找不到該表單，請聯絡開發人員")
        table = parse_google_sheet(sheet.URL, sheet.SID, sheet.CNAME, sheet.VIP)
        amount = len(table) - 1
        return render(request, 'GoogleSheet/sheet.html', locals())

    else:
        sheet = GoogleSheet.objects.all()

    return render(request, 'GoogleSheet/list.html', locals())
