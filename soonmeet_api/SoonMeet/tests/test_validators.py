from unittest import TestCase

from rest_framework.serializers import ValidationError

from SoonMeet.validators.not_equal import validate_not_equal


class TestValidators(TestCase):
    """ Class for testing validators in validators module. """

    def test_not_equal(self):
        """ Test if validator raises an error if numbers are equal. """
        self.assertIsNone(validate_not_equal(1, 2))
        self.assertIsNone(validate_not_equal(-1, 1))
        self.assertIsNone(validate_not_equal(5, 213))

        with self.assertRaises(ValidationError):
            validate_not_equal(1, 1)
            validate_not_equal(0, 0)
            validate_not_equal(-1, -1)
            validate_not_equal(99, 99)

    def test_start_before_end(self):
        """ Test if validator raises an error if start timestamp is after end timestamp. """
        pass
