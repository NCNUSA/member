from django.shortcuts import render
from django.db.models import Q
import operator
from functools import reduce
from .models import Member, GP, GPM
from django.http import HttpResponse

# Create your views here.

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
    SAM = GPM.objects.filter(GP__GNAME='學生會')
    return render(request, 'SA.html', locals())
