from django.core.management.base import BaseCommand, CommandError

from backend.models import Member

# import file path
PATH = ""
# define indicator
degree = ["學", "碩", "博"]
status = ["1", "2", "3", "4", "5", "6", "7", "8", "畢業", "退學", "休學"]
degree_status = []
for i in degree:
    for j in status:
        degree_status.append(i + j)


class Command(BaseCommand):
    help = "import member into database"

    def add_arguments(self, parser):
        parser.add_argument("stu_year", nargs="+", type=int)

    def handle(self, *args, **options):
        for stu_year in options["stu_year"]:
            global PATH
            # open file
            PATH = PATH + str(stu_year)
            f = open(PATH, "r")
            for i in f.readlines():
                t = i.split()
                for ds in degree_status:
                    if ds in t[2]:
                        pos = t[2].find(ds)
                        grade = t[2][pos:]
                        dep = t[2][:pos]
                        sid = t[0]
                        cname = t[1]
                        if not Member.objects.filter(SID=sid).exists():
                            Member.objects.create(SID=sid, CNAME=cname, DEP=dep, GRADE=grade)
                    else:
                        continue
        self.stdout.write(self.style.SUCCESS("done!"))
