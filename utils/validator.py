from django.core.exceptions import ValidationError
from django.db import models
from abc import ABCMeta, abstractmethod
import re


class ValidatorBase(metaclass=ABCMeta):
    def __init__(self, model_obj: models.Model):
        self._model_obj = model_obj

    @abstractmethod
    def execute(self):
        pass


class FieldFormatValidator:
    @staticmethod
    def execute(field, re_pattern: str, error_msg: str):
        result = re.match(re_pattern, field)

        if result is None:
            raise ValidationError(error_msg)
