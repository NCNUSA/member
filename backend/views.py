from django.shortcuts import render, redirect
from django.db.models import Q
import operator
from functools import reduce
from .models import Member, GP, GPM
from django.http import HttpResponse
from django.core.validators import validate_email

# 類 Google 搜尋，採用 AND
def Qfunction(query):
    QQuery = None
    for i in query:
        if QQuery == None:
            QQuery = Q(Q(SID__contains=i) | Q(GRADE__contains=i) | Q(DEP__contains=i) | Q(CNAME__contains=i))
        else:
            QQuery &= Q(Q(SID__contains=i) | Q(GRADE__contains=i) | Q(DEP__contains=i) | Q(CNAME__contains=i))
    return QQuery

def index(request):
    if 'Q' in request.GET:
        query = request.GET['Q'].strip().split()
        result = Member.objects.filter( Qfunction(query) )
        return render(request, 'index.html', locals())
    else:
        return render(request, 'index.html')
#        return HttpResponse("")

def SA(request):
    '''秀出學生會名單'''
    SAM = GPM.objects.filter(GP__GNAME='學生會')
    return render(request, 'SA.html', locals())

def edit(request, gp=0, sid=0):
    '''編輯群組成員的職稱'''
    if gp!=0 and sid!=0:
        user = GPM.objects.get(GP__id=gp, MEMBER__SID=sid)
        return render(request, 'edit.html', locals())
    else:
        if 'gp' in request.POST and 'sid' in request.POST:
            gp = request.POST['gp'].strip()
            sid = request.POST['sid'].strip()
            title = request.POST['title'].strip()
            email = request.POST['email'].strip()
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
        return redirect('SA')
    
def GPedit(request, gp):
    '''編輯群組成員'''
    if request.method == 'POST':
        gp = request.POST['gp'].strip()
        add = request.POST['add'].strip().split(',')
        remove = request.POST['remove'].strip().split(',')
        gp = GP.objects.get(id=gp)
        # return HttpResponse(add[0])
        for i in add:
            sid = i.strip()
            if sid.strip() != '' and Member.objects.filter(SID=sid).exists() and not GPM.objects.filter(GP=gp, MEMBER__SID=sid).exists():
                m = Member.objects.get(SID=sid)
                GPM.objects.create(GP=gp, MEMBER=m)
        for i in remove:
            sid = i.strip()
            if sid.strip() != '' and Member.objects.filter(SID=sid).exists() and GPM.objects.filter(GP=gp, MEMBER__SID=sid).exists():
                GPM.objects.filter(GP=gp, MEMBER__SID=sid).delete()
        return redirect('SA')
    return render(request, 'GPedit.html', locals())
