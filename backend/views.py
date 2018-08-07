from django.shortcuts import render
from django.db.models import Q
import operator
from functools import reduce
from .models import Member
from django.http import HttpResponse

# Create your views here.

def index(request):
    if 'Q' in request.GET:
        q = request.GET['Q']
        query = q.strip()
        result = Member.objects.filter( Q(SID__contains=query) | Q(GRADE__contains=query) )
#        C = Member.objects.filter( Q(reduce(operator.or_, (Q(SID__contains=x) for x in query_list))) & Q(reduce(operator.or_, (Q(GRADE__contains=x) for x in query_list))))
        return render(request, 'index.html', locals())
    else:
        return render(request, 'index.html')
#        return HttpResponse("")
