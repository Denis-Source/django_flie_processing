import string
from logging import getLogger
from random import choices

from django.test import TestCase

from log_record.models import LogRecord


class LogRecordTestCase(TestCase):
    def setUp(self) -> None:
        self.logger = getLogger()

        self.test_message = "test message"

        self.level_map = {
            10: self.logger.debug,
            20: self.logger.info,
            30: self.logger.warning,
            40: self.logger.error,
            50: self.logger.critical,
        }

    def test_record_is_created_when_logged(self):
        self.logger.setLevel(0)
        self.logger.info(self.test_message)
        record = LogRecord.objects.get(message=self.test_message)
        self.assertIsInstance(record, LogRecord)

    def test_all_levels_are_saved(self):
        self.logger.setLevel(0)
        for level, method in self.level_map.items():
            method(self.test_message)

        records = LogRecord.objects.filter(message=self.test_message)
        self.assertEqual(len(records), len(self.level_map))

    def test_only_higher_than_set_record_logged(self):
        levels = list(self.level_map.keys())
        expected = 0

        for level in levels:
            level -= 10
            self.logger.setLevel(level)
            for c_level, method in self.level_map.items():
                method(self.test_message)
                expected += c_level >= level

        records = LogRecord.objects.filter(message=self.test_message)
        self.assertEqual(len(records), expected)


