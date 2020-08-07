from rest_framework.validators import ValidationError
from django.db.models import DateField, TimeField


def validate_start_before_end(start_date: DateField,
                              end_date: DateField,
                              start_time: TimeField,
                              end_time: TimeField,
                              message='Validation error: event start time is sooner that end time'):
    """
    Validate that the start timestamp is earlier that the end timestamp.
    :param start_date: date of start
    :param end_date: date of end
    :param start_time: time of start
    :param end_time: time of end
    :param message: message raised upon ValidationError
    :return: None if validation passed
    """
    if start_date == end_date:
        if start_time > end_time:
            raise ValidationError(message)
    elif start_date > end_date:
        raise ValidationError(message)
