from utils.validator import ValidatorBase, FieldFormatValidator
from django.db import models


class Validator(ValidatorBase):
    def __init__(self, model_obj: models):
        super().__init__(model_obj)

    def execute(self):
        self.__strip()
        self.__check_field_is_not_empty()

    def __strip(self):
        fields = ["CNAME", "ENAME"]
        for field in fields:
            value = getattr(self._model_obj, field)
            setattr(self._model_obj, field, value.strip())

    def __check_field_is_not_empty(self):
        rules = {
            "SID": "^\d+$",  # positive integer
        }
        for field, pattern in rules.items():
            value = str(getattr(self._model_obj, field))
            FieldFormatValidator.execute(value, pattern,
                                         f"field '{field}': '{value}' is not allowed")
