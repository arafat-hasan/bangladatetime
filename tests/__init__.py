#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import csv
import unittest

BASEDIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, BASEDIR)

import bangladatetime

NUMBER_OF_LEAP_YEARS_BEFORE = [0]
cnt = 0
for i in range(1, 99999):
    cnt = cnt + bangladatetime._is_leap(i)
    NUMBER_OF_LEAP_YEARS_BEFORE.append(cnt)


def _ans_of_days_before_year(year):
    real = (year - 1) * 365 + NUMBER_OF_LEAP_YEARS_BEFORE[year - 1]
    return real


class Testbangladatetime(unittest.TestCase):

    def test_fromgregorian(self):
        with open('tests/data/2019-2020.csv', encoding="utf16") as file:
            has_header = csv.Sniffer().has_header(file.read(1024))
            file.seek(0)
            reader = csv.reader(file)
            if has_header:
                next(reader)

            data = tuple((str(row[0]), str(row[1])) for row in reader)

        for (gregorian, bangla) in data:
            gregorian_year, gregorian_month, gregorian_day = \
                bangladatetime._parse_isoformat_date(gregorian)

            bangla_year, bangla_month, bangla_day = \
                bangladatetime._parse_isoformat_date(bangla)

            calc = bangladatetime.date.fromgregorian(gregorian_year,
                                                      gregorian_month,
                                                      gregorian_day)

            self.assertEqual((calc.year, calc.month, calc.day),
                             (bangla_year, bangla_month, bangla_day))

    def test_is_leap_year(self):
        errorMsg = "Test failed with bangla year: "
        test_year_list = ((1406, True), (1422, True), (1306, False), (1426,
                                                                      True))

        for (year, ans) in test_year_list:
            _flag = bangladatetime._is_leap(year)
            self.assertEqual(_flag, ans, errorMsg + str(year))

    def test_days_before_year(self):
        errorMsg = "Test failed with bangla year: "
        for year in range(1, 9999):
            ret = bangladatetime._days_before_year(year)
            ans = (year - 1) * 365 + NUMBER_OF_LEAP_YEARS_BEFORE[year - 1]
            self.assertEqual(ans, ret, errorMsg + str(year))


if __name__ == "__main__":
    unittest.main()
