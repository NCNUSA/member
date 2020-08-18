from django.db import models


class UserPerms(models.Model):
    from django.contrib.auth.models import User
    from backend.models import Group
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gp = models.ForeignKey(Group, on_delete=models.CASCADE)
    edit = models.BooleanField()

    def __str__(self):
        message = "不可編輯"
        if self.edit:
            message = "可編輯"
        return str(self.user) + " " + str(self.gp) + " " + message
