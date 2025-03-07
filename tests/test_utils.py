import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from constance.management.commands.constance import _set_constance_value
from constance.utils import get_values
from constance.utils import get_values_for_keys


class UtilsTestCase(TestCase):
    def test_set_value_validation(self):
        self.assertRaisesMessage(ValidationError, 'Enter a whole number.', _set_constance_value, 'INT_VALUE', 'foo')
        self.assertRaisesMessage(
            ValidationError, 'Enter a valid email address.', _set_constance_value, 'EMAIL_VALUE', 'not a valid email'
        )
        self.assertRaisesMessage(
            ValidationError,
            'Enter a valid date.',
            _set_constance_value,
            'DATETIME_VALUE',
            (
                '2000-00-00',
                '99:99:99',
            ),
        )
        self.assertRaisesMessage(
            ValidationError,
            'Enter a valid time.',
            _set_constance_value,
            'DATETIME_VALUE',
            (
                '2016-01-01',
                '99:99:99',
            ),
        )

    def test_get_values(self):
        self.assertEqual(
            get_values(),
            {
                'FLOAT_VALUE': 3.1415926536,
                'BOOL_VALUE': True,
                'EMAIL_VALUE': 'test@example.com',
                'INT_VALUE': 1,
                'CHOICE_VALUE': 'yes',
                'TIME_VALUE': datetime.time(23, 59, 59),
                'DATE_VALUE': datetime.date(2010, 12, 24),
                'TIMEDELTA_VALUE': datetime.timedelta(days=1, hours=2, minutes=3),
                'LINEBREAK_VALUE': 'Spam spam',
                'DECIMAL_VALUE': Decimal('0.1'),
                'STRING_VALUE': 'Hello world',
                'DATETIME_VALUE': datetime.datetime(2010, 8, 23, 11, 29, 24),
                'LIST_VALUE': [1, '1', datetime.date(2019, 1, 1)],
                'JSON_VALUE': {
                    'key': 'value',
                    'key2': 2,
                    'key3': [1, 2, 3],
                    'key4': {'key': 'value'},
                    'key5': datetime.date(2019, 1, 1),
                    'key6': None,
                },
                'DERIVED_VALUE_FUNC': 'Hello world to test@example.com',
                'DERIVED_VALUE_FUNC_STR': 'Hello world to test@example.com',
                'DERIVED_VALUE_LAMBDA': 'Hello world to test@example.com',
            },
        )

    def test_get_values_for_keys(self):
        self.assertEqual(
            get_values_for_keys(['BOOL_VALUE', 'CHOICE_VALUE', 'LINEBREAK_VALUE']),
            {
                'BOOL_VALUE': True,
                'CHOICE_VALUE': 'yes',
                'LINEBREAK_VALUE': 'Spam spam',
            },
        )

    def test_get_values_for_keys_empty_keys(self):
        result = get_values_for_keys([])
        self.assertEqual(result, {})

    def test_get_values_for_keys_throw_error_if_no_key(self):
        self.assertRaisesMessage(
            AttributeError,
            '"OLD_VALUE, BOLD_VALUE" keys not found in configuration.',
            get_values_for_keys,
            ['BOOL_VALUE', 'OLD_VALUE', 'BOLD_VALUE'],
        )

    def test_get_values_for_keys_invalid_input_type(self):
        with self.assertRaises(TypeError):
            get_values_for_keys('key1')
