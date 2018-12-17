from django import forms
from django.utils.translation import gettext as _


class ColPositionField(forms.IntegerField):
    def to_python(self, value):
        """Normalize data to an Integer"""

        if value.isdigit():
            return int(value)
        elif value is '':
            return 0
        else:
            raise forms.ValidationError(
                _('Invalid value,%(value)s 請輸入 0~50 間整數'),
                code='invalid',
                params={'value': value},
            )

    def validate(self, value):
        """Check if the number is valid, e.g., >=0 & <=50."""

        super(ColPositionField, self).validate(value)
        if value < 0 or value > 50:
            raise forms.ValidationError(
                _('Invalid value: %(value)s. 請輸入 0~50'),
                code='invalid',
                params={'value': value},
            )


class SheetCheckForm(forms.Form):
    sid = ColPositionField(label='學號位置', required=False)
    email = ColPositionField(label='電郵位置', required=False)
    is_member = ColPositionField(label='是否為會員位置', required=False)
    name = ColPositionField(label='姓名位置', required=False)
    spreadsheet = forms.FileField(label='試算表')

    def clean_spreadsheet(self):
        data = self.cleaned_data['spreadsheet']

        # file size should > 1 MB
        if data.size > 1024*1024:
            raise forms.ValidationError(
                _('檔案過大，請使用小於 1 MB 的檔案'),
            )
        # file type should be xlsx or xls
        if not (data.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                or data.content_type == 'application/vnd.ms-excel'):
            raise forms.ValidationError(
                _('請上傳 xls/xlsx 格式之檔案'),
            )
        return data
