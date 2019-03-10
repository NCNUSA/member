from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


class MemberManager(models.Manager):
    def name_check(self, sid, cname):
        try:
            record = self.get(SID=sid).CNAME
        except Member.DoesNotExist:
            raise ValueError('SID is wrong')

        if record != cname:
            return record
        else:
            return True

    @staticmethod
    def mail_validation(email):
        """檢查 *學生* 的信箱是否填寫正確"""
        try:
            validate_email(email)
            black_list = [
                '@gmail.com.tw',
                '@gmial.com',
                '@mai1.ncnu.edu.tw',
            ]
            for b in black_list:
                if b in email:
                    raise ValidationError('domain name error')
            # 學生應該要是 mail1 而不是 mail
            regex = re.compile(r'10[0-9]{7}@mail.ncnu.edu.tw')
            if regex.search(email) is not None:
                raise ValidationError('domain name error')
        except ValidationError:
            raise

    def query_member(self, query):
        """類 Google 搜尋，採用 AND"""
        from django.db.models import Q

        QQuery = None
        for i in query:
            if QQuery is None:
                QQuery = Q(Q(SID__contains=i) | Q(GRADE__contains=i) | Q(
                    DEP__contains=i) | Q(CNAME__contains=i))
            else:
                QQuery &= Q(Q(SID__contains=i) | Q(GRADE__contains=i) | Q(
                    DEP__contains=i) | Q(CNAME__contains=i))
        return self.filter(QQuery)

    def sheet_check(self, gp, data, sid_pos, name_pos, email_pos, is_member_pos):
        # handle table columns
        table = data.sheets()[0]
        sid_col = table.col_values(sid_pos - 1)[1:]
        member_sign_col = table.col_values(is_member_pos - 1)[1:]
        name_col = table.col_values(name_pos - 1)[1:]
        email_col = table.col_values(email_pos - 1)[1:]
        # init msg which will show in front end
        gp_error, email_list = '', ''
        sid_error, member_error, name_error, email_error = [], [], [], []
        for key, row in enumerate(sid_col):
            # 強制將 float 轉型成 str, e.g. '104321031.0'
            try:
                sid = str(int(float(row)))
            except ValueError:
                sid_error.append(row)
                continue
            try:
                # member_check
                if Group.objects.member_check(sid=sid, gp=str(gp)):
                    if member_sign_col[key] == '否':
                        # 是會員填成否
                        member_error.append((sid, 1))
                else:
                    if member_sign_col[key] == '是':
                        # 不是會員填成是
                        member_error.append((sid, 2))
                # name check
                if name_pos != 0:
                    record_name = self.name_check(sid=sid,
                                                  cname=name_col[key])
                    if type(record_name) == str:
                        name_error.append((sid, name_col[key], record_name))
                # email list
                if email_pos != 0:
                    try:
                        self.mail_validation(email_col[key])
                        email_list += email_col[key] + ', '
                    except:
                        email_error.append((sid, email_col[key]))
            except ValueError:
                # 學號錯誤
                sid_error.append(sid)
            except LookupError:
                gp_error += str(gp)
                break
        return gp_error, email_list, sid_error, member_error, name_error, email_error


class Member(models.Model):
    SID = models.CharField( max_length=10, unique=True, verbose_name='學號')
    CNAME = models.CharField( max_length=20, verbose_name='中文姓名')
    ENAME = models.CharField( max_length=100, blank=True, null=True, verbose_name='英文姓名')
    DEP = models.CharField( max_length=30, blank=True, null=True, verbose_name='系所')
    GRADE = models.CharField( max_length=10, blank=True, null=True, verbose_name='年級')
    EMAIL = models.EmailField( blank=True, null=True)
    PHONE = models.CharField( max_length=20, blank=True, null=True, verbose_name='手機')
    EXT = models.CharField( max_length=20, blank=True, null=True, verbose_name='校內分機')
    ICN = models.CharField( max_length=15, blank=True, null=True, verbose_name='身份證字號')
    ADDR = models.CharField( max_length=200, blank=True, null=True, verbose_name='住址')
    created_at = models.DateTimeField( auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField( auto_now=True, verbose_name='修改時間')
    objects = MemberManager()

    def __str__(self):
        return self.SID + ' ' + self.CNAME


class GroupManager(models.Manager):
    def member_check(self, sid, gp):
        try:
            gp = self.get(id=gp)
        except Group.DoesNotExist:
            raise LookupError('GP is wrong')

        try:
            m = Member.objects.get(SID=sid)
        except Member.DoesNotExist:
            raise ValueError('SID is wrong')

        if GroupMember.objects.filter(MEMBER=m, GP=gp).exists():
            return True
        else:
            return False

    @staticmethod
    def group_list(uid):
        """Get a list of the group the user manage
        Args:
            uid: The user's account id

        Returns:
            list
        """
        gp_list = []
        for item in UserPerms.objects.filter(user=uid):
            gp_list.append(item.gp)
        return gp_list


class Group(models.Model):
    GNAME = models.CharField( max_length=30, verbose_name='社團名稱')
    created_at = models.DateTimeField( auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField( auto_now=True, verbose_name='建立時間')
    users = models.ManyToManyField(
        User,
        through='UserPerms',
        related_name='perms'
    )
    objects = GroupManager()
    
    def __str__(self):
        return self.GNAME


class UserPerms(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gp = models.ForeignKey(Group, on_delete=models.CASCADE)
    edit = models.BooleanField()

    def __str__(self):
        message = '不可編輯'
        if self.edit:
            message = '可編輯'
        return str(self.user) + ' ' + str(self.gp) + ' ' + message


class GroupMemberManager(models.Manager):
    def member_update(self, sid, gp, title, email, phone):
        user = self.get(GP__id=gp, MEMBER__SID=sid)
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

    def member_list_update(self, gp, add, remove):
        """編輯群組成員名單

        Args:
            gp: Target group's id
            add(list): SID in list, e.g., ['104321001', '105321001']
            remove(list): SID in list, like above one.
        """
        for i in add:
            sid = i.strip()
            if sid.strip() != '' and Member.objects.filter(SID=sid).exists()\
                and not self.filter(GP=gp, MEMBER__SID=sid).exists():
                m = Member.objects.get(SID=sid)
                self.create(GP=gp, MEMBER=m)
        for i in remove:
            sid = i.strip()
            if sid.strip() != '' and Member.objects.filter(SID=sid).exists() and self.filter(GP=gp, MEMBER__SID=sid).exists():

                    self.filter(GP=gp, MEMBER__SID=sid).delete()


class GroupMember(models.Model):
    MEMBER = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='成員')
    GP = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='群組')
    TITLE = models.CharField( max_length=15,blank=True, null=True, verbose_name='職稱')
    RM = models.CharField( max_length=30, blank=True, null=True, verbose_name='備註')
    created_at = models.DateTimeField( auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField( auto_now=True, verbose_name='建立時間')
    objects = GroupMemberManager()

    def __str__(self):
        return self.GP.GNAME + ' ' + self.MEMBER.CNAME


class College(models.Model):
    CNAME = models.CharField( max_length=30, verbose_name='中文名稱')
    ENAME = models.CharField( max_length=200, blank=True, null=True, verbose_name='英文名稱')
    CABBR = models.CharField( max_length=10, blank=True, null=True, verbose_name='中文簡稱')
    EABBR = models.CharField( max_length=30, blank=True, null=True, verbose_name='英文簡稱')

    def __str__(self):
        return self.CABBR


class Department(models.Model):
    CNAME = models.CharField( max_length=30, verbose_name='中文名稱')
    ENAME = models.CharField( max_length=200, blank=True, null=True, verbose_name='英文名稱')
    CABBR = models.CharField( max_length=10, blank=True, null=True, verbose_name='中文簡稱')
    EABBR = models.CharField( max_length=30, blank=True, null=True, verbose_name='英文簡稱')
    COLLEGE = models.ForeignKey(College, related_name='DEP', on_delete=models.CASCADE, verbose_name='學院')

    def __str__(self):
        return self.CABBR


class GoogleSheet(models.Model):
    TITLE = models.CharField( max_length=100 )
    URL = models.URLField( max_length=200, verbose_name='目標網址')
    SID = models.IntegerField( verbose_name='學號欄位', blank=True, null=True )
    CNAME = models.IntegerField( verbose_name='中文名稱欄位', blank=True, null=True)
    VIP = models.IntegerField( verbose_name='是否為學生會員欄位', blank=True, null=True )
    EMAIL = models.IntegerField( verbose_name='EMAIL 在第幾欄', blank=True, null=True )
    GP = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.GP.GNAME + ' - ' + self.TITLE
