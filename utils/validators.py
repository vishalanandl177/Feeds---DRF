"""
    File:           validators.py
    Description:    Use the function to validate inputs in models.
"""
import datetime

from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def text_validator(text):
    if len(text) < 5:
        raise ValidationError(
            _('Length must be greater than 4')
        )


def email_validator(email):
    if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email) is None:
        raise ValidationError(
            _('Invalid email address')
        )


def mobile_number_validator(text):
    if re.match("^[6-9][0-9]{9}$", text) is None:
        raise ValidationError(
            _('Invalid mobile number')
        )


def country_code_validator(text):
    if re.match("^(\+)[1-9][0-9]?$", text) is None:
        raise ValidationError(
            _('Invalid country code')
        )


def imei_validator(text):
    if re.match("^[1-9][0-9]{14, 44}*$", text) is None:
        raise ValidationError(
            _('Invalid IMEI number')
        )


def string_validator(text):
    if re.match('^[a-zA-Z]+$', text) is None:
        raise ValidationError(
            _('Only alphabets are allowed (no space)')
        )


def string_with_space_validator(text):
    if re.match('^[ a-zA-Z]+$', text) is None:
        raise ValidationError(
            _('Only alphabets are allowed')
        )


def number_validator(text):
    if re.match('^[1-9]+[0-9]*$', str(text)) is None:
        raise ValidationError(
            _('Only numbers are allowed')
        )


def string_number_validator(text):
    if re.match('^[a-zA-Z0-9]+$', str(text)) is None:
        raise ValidationError(
            _('Only number and characters are allowed')
        )


def upi_validator(text):
    if re.match('^[\w]*[@][\w]*$', str(text)) is None:
        raise ValidationError(
            _('Invalid UPI')
        )


def percentage_validator(number):
    if number < 0 or number > 100:
        raise ValidationError(
            _('Invalid percentage')
        )


def no_past_date_time_validator(value):
    if value > timezone.now():
        raise ValidationError('Date cannot be in the past.')


def no_past_date_validator(value):
    if value < datetime.datetime.now().date():
        raise ValidationError('Date cannot be in the past.')
