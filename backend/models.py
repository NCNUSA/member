from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
# from django.conf import settings


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

    def mail_validattion(self, email):
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


class GPManager(models.Manager):
    def member_check(self, sid, gp):
        try:
            gp = self.get(id=gp)
        except GP.DoesNotExist:
            raise LookupError('GP is wrong')

        try:
            m = Member.objects.get(SID=sid)
        except Member.DoesNotExist:
            raise ValueError('SID is wrong')

        if GPM.objects.filter(MEMBER=m, GP=gp).exists():
            return True
        else:
            return False


class GP(models.Model):
    GNAME = models.CharField( max_length=30, verbose_name='社團名稱')
    created_at = models.DateTimeField( auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField( auto_now=True, verbose_name='建立時間')
    users = models.ManyToManyField(
        User,
        through='UserPerms',
        # through_fields=('user', 'gp'),
        related_name ='perms'
    )
    objects = GPManager()
    
    def __str__(self):
        return self.GNAME


class UserPerms(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gp = models.ForeignKey(GP, on_delete=models.CASCADE)
    edit = models.BooleanField()

    def __str__(self):
        message = '不可編輯'
        if self.edit:
            message = '可編輯'
        return str(self.user) + ' ' + str(self.gp) + ' ' + message


class GPM(models.Model):
    MEMBER = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='成員')
    GP = models.ForeignKey(GP, on_delete=models.CASCADE, verbose_name='群組')
    TITLE = models.CharField( max_length=15,blank=True, null=True, verbose_name='職稱')
    RM = models.CharField( max_length=30, blank=True, null=True, verbose_name='備註')
    created_at = models.DateTimeField( auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField( auto_now=True, verbose_name='建立時間')

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
    GP = models.ForeignKey(GP, on_delete=models.CASCADE)

    def __str__(self):
        return self.GP.GNAME + ' - ' + self.TITLE
