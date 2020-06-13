#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import sys
# import os
import csv
import unittest
from collections import Counter

# BASEDIR = os.path.abspath(
#     os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
# sys.path.insert(0, BASEDIR)

import bangladatetime.date
from bangladatetime.date import _is_leap
from bangladatetime.date import _days_before_year, _parse_isoformat_date
from bangladatetime.date import _days_in_month, _ord2md, _ymd2ord

_DAYS_IN_BANGLA_MONTH = [-1, 31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 29, 30]

NUMBER_OF_LEAP_YEARS_BEFORE = [0]
cnt = 0
for i in range(1, 99999):
    cnt = cnt + _is_leap(i)
    NUMBER_OF_LEAP_YEARS_BEFORE.append(cnt)


def _ans_of_days_before_year(year):
    real = (year - 1) * 365 + NUMBER_OF_LEAP_YEARS_BEFORE[year - 1]
    return real


class Testbangladatetime(unittest.TestCase):
    def test_fromgregorian(self):
        """
        Test that it can sum a list of integers
        """
        with open('tests/2019-2020.csv', encoding="utf16") as file:
            has_header = csv.Sniffer().has_header(file.read(1024))
            file.seek(0)
            reader = csv.reader(file)
            if has_header:
                next(reader)

            data = tuple((str(row[0]), str(row[1])) for row in reader)

        for (gregorian, bangla) in data:
            gregorian_year, gregorian_month, gregorian_day = \
                _parse_isoformat_date(gregorian)

            bangla_year, bangla_month, bangla_day = _parse_isoformat_date(
                bangla)

            calc = bangladatetime.date.fromgregorian(gregorian_year,
                                                     gregorian_month,
                                                     gregorian_day)

            self.assertEqual((calc.year, calc.month, calc.day),
                             (bangla_year, bangla_month, bangla_day))

    def test_is_leap_year(self):
        """
        Test that it can sum a list of integers
        """
        errorMsg = "Test failed with bangla year: "
        test_year_list = ((1406, True), (1422, True), (1306, False), (1426,
                                                                      True))

        for (year, ans) in test_year_list:
            _flag = _is_leap(year)
            self.assertEqual(_flag, ans, errorMsg + str(year))

    def test_days_before_year(self):
        """
        Test that it can sum a list of integers
        """
        errorMsg = "Test failed with bangla year: "
        for year in range(1, 9999):
            ret = _days_before_year(year)
            ans = (year - 1) * 365 + NUMBER_OF_LEAP_YEARS_BEFORE[year - 1]
            self.assertEqual(ans, ret, errorMsg + str(year))

    def test_ord2md(self):
        non_leap_list = []
        for i in range(1, 366):
            non_leap_list.append(_ord2md(1427, i))

        duplicates = Counter(non_leap_list)
        self.assertEqual(len(duplicates), 365, "Failed in a non leap year")

        leap_list = []
        for i in range(1, 367):
            leap_list.append(_ord2md(1426, i))

        duplicates = Counter(leap_list)
        self.assertEqual(len(duplicates), 366, "Failed in a leap year")

    def test_fromordinal(self):
        """
        Test that it can sum a list of integers
        """
        errorMsg = "Test failed with bangla year: "
        ordinaldate = 0
        for year in range(1, 9999):
            for month in range(1, 13):
                days = _days_in_month(year, month)
                for day in range(1, days + 1):
                    ordinaldate = ordinaldate + 1
                    test = bangladatetime.date.fromordinal(ordinaldate)
                    self.assertEqual((test.year, test.month, test.day),
                                     (year, month, day), errorMsg + str(year))

    def test_ymd2ord(self):
        """
        Test that it can sum a list of integers
        """
        errorMsg = "Test failed with bangla year: "
        ordinaldate = 0
        for year in range(1, 9999):
            for month in range(1, 13):
                days = _days_in_month(year, month)
                for day in range(1, days + 1):
                    ordinaldate = ordinaldate + 1
                    test = _ymd2ord(year, month, day)
                    self.assertEqual(ordinaldate, test, errorMsg + str(year))


if __name__ == "__main__":
    unittest.main()
