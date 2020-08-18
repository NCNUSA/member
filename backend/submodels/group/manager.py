from django.db.models import Manager
from django.core.exceptions import ObjectDoesNotExist


class GroupManager(Manager):
    def member_check(self, sid, gp):
        from backend.models import GroupMember, Member

        try:
            gp = self.get(id=gp)
        except ObjectDoesNotExist:
            raise LookupError("GP is wrong")

        try:
            m = Member.objects.get(SID=sid)
        except Member.DoesNotExist:
            raise ValueError("SID is wrong")

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
        from backend.models import UserPerms

        gp_list = []
        for item in UserPerms.objects.filter(user=uid):
            gp_list.append(item.gp)
        return gp_list
