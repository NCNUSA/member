from django.db.models import Manager
from django.core.validators import validate_email


class GroupMemberManager(Manager):
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
            m.PHONE = phone.replace("-", "")
            m.save()

    def member_list_update(self, gp, add, remove):
        """編輯群組成員名單

        Args:
            gp: Target group's id
            add(list): SID in list, e.g., ['104321001', '105321001']
            remove(list): SID in list, like above one.
        """
        from backend.models import Member
        for i in add:
            sid = i.strip()
            if (
                sid.strip() != ""
                and Member.objects.filter(SID=sid).exists()
                and not self.filter(GP=gp, MEMBER__SID=sid).exists()
            ):
                m = Member.objects.get(SID=sid)
                self.create(GP=gp, MEMBER=m)
        for i in remove:
            sid = i.strip()
            if (
                sid.strip() != ""
                and Member.objects.filter(SID=sid).exists()
                and self.filter(GP=gp, MEMBER__SID=sid).exists()
            ):
                self.filter(GP=gp, MEMBER__SID=sid).delete()
