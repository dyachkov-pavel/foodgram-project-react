from django.core.exceptions import ValidationError


def validate_time(value):
    if value <= 0:
        raise ValidationError('Время должно быть больше нуля!')


def validate_more_than_zero(value):
    if value <= 0:
        raise ValidationError('Количество должно быть больше нуля!')
