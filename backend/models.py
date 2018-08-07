from django.db import models

# Create your models here.

class Member(models.Model):
    ID = models.AutoField( primary_key=True )
    SID = models.CharField( max_length=10, unique=True )
    CNAME = models.CharField( max_length=20 )
    ENAME = models.CharField( max_length=100, blank=True, null=True )
    DEP = models.CharField( max_length=30, blank=True, null=True )
    GRADE = models.CharField( max_length=10, blank=True, null=True )
    EMAIL = models.EmailField( blank=True, null=True )
    PHONE = models.CharField( max_length=20, blank=True, null=True )
    EXT = models.CharField( max_length=20, blank=True, null=True )
    ICN = models.CharField( max_length=15, blank=True, null=True )
    ADDR = models.CharField( max_length=200, blank=True, null=True )
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )

    def __str__(self):
        return self.SID + ' ' + self.CNAME
