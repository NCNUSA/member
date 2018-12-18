from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
from django.http import HttpResponse
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.conf import settings
import xlrd
import datetime
from django.core.files.storage import FileSystemStorage
from .forms import SheetCheckForm


def Qfunction(query):
    """類 Google 搜尋，採用 AND"""
    QQuery = None
    for i in query:
        if QQuery is None:
            QQuery = Q(Q(SID__contains=i) | Q(GRADE__contains=i) | Q(DEP__contains=i) | Q(CNAME__contains=i))
        else:
            QQuery &= Q(Q(SID__contains=i) | Q(GRADE__contains=i) | Q(DEP__contains=i) | Q(CNAME__contains=i))
    return QQuery


@login_required
def index(request):
    if 'Q' in request.GET:
        query = request.GET['Q'].strip().split()
        result = Member.objects.filter(Qfunction(query))
        return render(request, 'index.html', locals())
    else:
        return render(request, 'index.html')


@login_required
def group_list(request):
    gp_list = []
    for item in UserPerms.objects.filter(user=request.user.id):
        gp_list.append(item.gp)
    # print(gp_list)
    # gp_list = GP.objects.all()
    return render(request, 'Group/list.html', locals())


@login_required
def group_detail(request, uid):
    if UserPerms.objects.filter(user=request.user.id, gp=uid):
        edit = UserPerms.objects.get(user=request.user.id, gp=uid).edit
        gp = GP.objects.get(id=uid)
        gp_member = GPM.objects.filter(GP__id=uid)
        return render(request, 'Group/detail.html', locals())
    else:
        return HttpResponse("無此權限")


@login_required
def edit(request, gp=0, sid=0):
    """編輯群組成員的職稱"""
    if UserPerms.objects.filter(user=request.user.id, gp=gp, edit=True):
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
    if UserPerms.objects.filter(user=request.user.id, gp=gp, edit=True):
        if request.method == 'POST':
            gp_id = request.POST['gp'].strip()
            add = request.POST['add'].strip().split(',')
            remove = request.POST['remove'].strip().split(',')
            gp = GP.objects.get(id=gp_id)
            for i in add:
                sid = i.strip()
                if sid.strip() != '' and Member.objects.filter(SID=sid).exists() and not GPM.objects.filter(GP=gp,
                                                                                                            MEMBER__SID=sid).exists():
                    m = Member.objects.get(SID=sid)
                    GPM.objects.create(GP=gp, MEMBER=m)
            for i in remove:
                sid = i.strip()
                if sid.strip() != '' and Member.objects.filter(SID=sid).exists() and GPM.objects.filter(GP=gp,
                                                                                                        MEMBER__SID=sid).exists():
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
    bsObj = BeautifulSoup(driver.page_source, "html.parser")
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
        table.remove([""] * len(table[0]))
    except:
        pass
    # 判斷姓名是否跟學號匹配
    if SID is not None and CNAME is not None:
        for index, row in enumerate(table):
            if index == 0:
                row.append("姓名是否匹配")
                continue
            try:
                m = Member.objects.get(SID=row[SID - 1])
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
        thead = table[0]
        tbody = table[1:]
        amount = len(tbody)
        SID, CNAME, VIP, EMAIL = sheet.SID, sheet.CNAME, sheet.VIP, sheet.EMAIL
        return render(request, 'GoogleSheet/sheet.html', locals())

    else:
        gp = UserPerms.objects.filter(user=request.user.id)
        gp_list = [i.gp for i in gp]
        sheet = GoogleSheet.objects.filter(GP__in=gp_list)
        return render(request, 'GoogleSheet/list.html', locals())


@login_required
def googleSheet_add(request):
    """新增 Google 表單的結果"""
    if request.method == "GET":
        gp = UserPerms.objects.filter(user=request.user.id)
        return render(request, 'GoogleSheet/add.html', locals())
    else:
        title = request.POST["title"]
        url = request.POST["url"]
        gp = request.POST["gp"]
        sid = request.POST["sid"]
        cname = request.POST["cname"]
        vip = request.POST["vip"]
        email = request.POST["email"]
        gp = GP.objects.get(id=gp)
        if cname == "":
            cname = None
        if vip == "":
            vip = None
        if sid == "":
            sid = None
        if title.strip() != "" and url.strip() != "":
            GoogleSheet.objects.create(TITLE=title, URL=url, GP=gp, SID=sid, CNAME=cname, VIP=vip, EMAIL=email)
        else:
            return HttpResponse("資料錯誤")
        return redirect(googleSheet)


@login_required
def googleSheet_edit(request, UID):
    """編輯表單基本資料"""
    if request.method == "GET":
        gp = UserPerms.objects.filter(user=request.user.id)
        gs = GoogleSheet.objects.get(id=UID)
        return render(request, 'GoogleSheet/edit.html', locals())
    elif request.method == "POST":
        title = request.POST["title"]
        url = request.POST["url"]
        gp = request.POST["gp"]
        sid = request.POST["sid"]
        cname = request.POST["cname"]
        vip = request.POST["vip"]
        email = request.POST["email"]
        gp = GP.objects.get(id=gp)
        if cname == "":
            cname = None
        if vip == "":
            vip = None
        if sid == "":
            sid = None
        if title.strip() != "" and url.strip() != "":
            gs = GoogleSheet.objects.get(id=request.POST["id"])
            gs.TITLE = title
            gs.URL = url
            gs.GP = gp
            gs.SID = sid
            gs.CNAME = cname
            gs.VIP = vip
            gs.EMAIL = email
            gs.save()
        else:
            return HttpResponse("資料錯誤")
        return redirect(googleSheet)


@login_required
def sheet_check(request):
    if request.method == 'POST':
        form = SheetCheckForm(request.POST, request.FILES)
        if form.is_valid():
            origin_name = form.cleaned_data['spreadsheet'].name
            fs = FileSystemStorage()
            dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            filename = fs.save(dt + '_' + origin_name, form.cleaned_data['spreadsheet'])
            url = fs.url(filename)
            data = xlrd.open_workbook(settings.MEDIA_ROOT + '/' + filename)
            table = data.sheets()[0]
            sid_pos = form.cleaned_data['sid']
            is_member__pos = form.cleaned_data['is_member']
            name_pos = form.cleaned_data['name']
            email_pos = form.cleaned_data['email']
            sid_col = table.col_values(sid_pos-1)[1:]
            member_sign_col = table.col_values(is_member__pos-1)[1:]
            name_col = table.col_values(name_pos-1)[1:]
            email_col = table.col_values(email_pos-1)[1:]
            wrong = ''
            email_list = ''
            for key, row in enumerate(sid_col):
                    # 強制將 float 轉型成 str, e.g. '104321031.0'
                    try:
                        sid = str(int(float(row)))
                    except ValueError:
                        wrong += row + ' 學號錯誤<br>'
                        continue
                    try:
                        # member_check
                        # gp=2 是付費會員
                        if GP.objects.member_check(sid=sid, gp=str(2)):
                            if member_sign_col[key] == '否':
                                wrong += sid + ' 是會員填成否<br>'
                        else:
                            if member_sign_col[key] == '是':
                                wrong += sid + ' 不是會員填成是<br>'
                        # name check
                        if name_pos != 0:
                            record_name = Member.objects.name_check(sid=sid, cname=name_col[key])
                            if type(record_name) == str:
                                wrong += sid + ' 的名字不該是 "' + name_col[key] + '"而是' + record_name + '"<br>'
                        # email list
                        if email_pos != 0:
                            email_list += email_col[key] + ', '
                    except ValueError:
                        wrong += sid + ' 學號錯誤<br>'
                    except LookupError:
                        wrong += 'GP 錯誤，找不到該 GP<br>若您不清楚錯誤，請聯絡開發人員'
                        break
            wrong = '<b>' + wrong + '</b>'

            return HttpResponse(wrong + '<br> <b>Email list:</b> ' + email_list)
        return render(request, 'xls_check/upload.html', locals())
    else:
        form = SheetCheckForm()
    return render(request, 'xls_check/upload.html', locals())
