# **WARNGIN**
# The code not test yet

from django.core.management.base import BaseCommand, CommandError
from backend.models import Member
import xlrd

# define indicator
degree = ['學', '碩', '博']
status = ['1', '2', '3', '4', '5', '6', '7', '8', '畢業', '退學', '休學']
degree_status = []
for i in degree:
    for j in status:
        degree_status.append(i+j)

def merge(list1, list2, list3):
    merged_list = [(p1, p2, p3) for idx1, p1 in enumerate(list1)
            for idx2, p2 in enumerate(list2) if idx1 == idx2
            for idx3, p3 in enumerate(list3) if idx1 == idx3]
    return merged_list


class Command(BaseCommand):
    help = 'import member into database from xls'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+', type=int)

    def handle(self, *args, **options):
        for path in options['filepath']:
            x = xlrd.open_workbook(path)
            xx = x.sheets()[0]
            t = merge(xx.col_values(1), xx.col_values(2), xx.col_values(0))
            t.pop(0)
            for i in t:
                if Member.objects.filter(SID=i[0]).exists():
                    pass
                else:
                    Member.objects.create(SID=i[0], CNAME=i[1], DEP=i[2])

        self.stdout.write(self.style.SUCCESS('done!'))
