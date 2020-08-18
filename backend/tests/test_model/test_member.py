from backend.models import Member
from django.core.exceptions import ValidationError
import pytest


@pytest.mark.django_db
def test_create_member():
    Member.objects.create(
        SID="108321000",
        CNAME="王小明"
    )


@pytest.mark.parametrize(
    "email",
    [
        "abc@gmail.com.tw",
        "abc@gmial.com",
        "abc@mai1.ncnu.edu.tw"
    ]
)
def test_mail_validation(email):
    with pytest.raises(ValidationError):
        Member.objects.mail_validation(email)
