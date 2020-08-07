from rest_framework.serializers import ValidationError


def validate_not_equal(first_value, second_value, invalid_values_message='Validation error: values are not equal.'):
    """
    Raise a ValidationError if compared values are equal.
    :param first_value: first value
    :param second_value: second value
    :param invalid_values_message: message upon raising ValidationError
    :return: None if validation passed
    """
    if first_value == second_value:
        raise ValidationError(invalid_values_message)
