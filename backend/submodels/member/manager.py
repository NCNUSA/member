from django.db.models import Manager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re


class MemberManager(Manager):
    def name_check(self, sid, cname):
        try:
            record = self.get(SID=sid).CNAME
        except super().DoesNotExist:
            raise ValueError("SID is wrong")

        if record != cname:
            return record
        else:
            return True

    @staticmethod
    def mail_validation(email):
        """檢查 *學生* 的信箱是否填寫正確"""
        try:
            validate_email(email)
            black_list = ["@gmail.com.tw", "@gmial.com", "@mai1.ncnu.edu.tw"]
            for b in black_list:
                if b in email:
                    raise ValidationError("domain name error")
            # 學生應該要是 mail1 而不是 mail
            regex = re.compile(r"10[0-9]{7}@mail.ncnu.edu.tw")
            if regex.search(email) is not None:
                raise ValidationError("domain name error")
        except ValidationError:
            raise

    def query_member(self, query):
        """類 Google 搜尋，採用 AND"""
        from django.db.models import Q

        QQuery = None
        for i in query:
            if QQuery is None:
                QQuery = Q(
                    Q(SID__contains=i)
                    | Q(GRADE__contains=i)
                    | Q(DEP__contains=i)
                    | Q(CNAME__contains=i)
                )
            else:
                QQuery &= Q(
                    Q(SID__contains=i)
                    | Q(GRADE__contains=i)
                    | Q(DEP__contains=i)
                    | Q(CNAME__contains=i)
                )
        return self.filter(QQuery)

    def sheet_check(self, gp, table, position):
        from backend.models import Group
        # handle table columns
        sid_col = table.col_values(position["sid_pos"] - 1)[1:]
        member_sign_col = table.col_values(position["is_member__pos"] - 1)[1:]
        name_col = table.col_values(position["name_pos"] - 1)[1:]
        email_col = table.col_values(position["email_pos"] - 1)[1:]
        # init msg which will show in front end
        gp_error, email_list = "", ""
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
                    if member_sign_col[key] == "否":
                        # 是會員填成否
                        member_error.append((sid, 1))
                else:
                    if member_sign_col[key] == "是":
                        # 不是會員填成是
                        member_error.append((sid, 2))
                # name check
                if position["name_pos"] != 0:
                    record_name = self.name_check(sid=sid, cname=name_col[key])
                    if type(record_name) == str:
                        name_error.append((sid, name_col[key], record_name))
                # email list
                if position["email_pos"] != 0:
                    try:
                        self.mail_validation(email_col[key])
                        email_list += email_col[key] + ", "
                    except:
                        email_error.append((sid, email_col[key]))
            except ValueError:
                # 學號錯誤
                sid_error.append(sid)
            except LookupError:
                gp_error += str(gp)
                break
        if (
            len(gp_error)
            == len(sid_error)
            == len(member_error)
            == len(name_error)
            == len(email_error)
            == 0
        ):
            no_error = True
        else:
            no_error = False
        result = {
            "name": table.name,
            "email_list": email_list,
            "gp_error": gp_error,
            "sid_error": sid_error,
            "member_error": member_error,
            "name_error": name_error,
            "email_error": email_error,
            "no_error": no_error,
        }
        return result
