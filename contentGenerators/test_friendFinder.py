from unittest import TestCase

import numpy as np

from contentGenerators.FriendFinder import FriendFinder


class TestFriendFinder(TestCase):

    def test_get_year_ok1(self):
        finder = FriendFinder()
        actual_year = finder.get_year("1.1.1111")
        expected = "1111"
        assert (actual_year == expected)

    def test_get_year_ok2(self):
        finder = FriendFinder()
        actual_year = finder.get_year("1..1111")
        expected = "1111"
        assert (actual_year == expected)

    def test_get_year_ok3(self):
        finder = FriendFinder()
        actual_year = finder.get_year(".1.1111")
        expected = "1111"
        assert (actual_year == expected)

    def test_get_year_bad1(self):
        finder = FriendFinder()
        actual_year = finder.get_year("1.1.")
        expected = ""
        assert (actual_year == expected)

    def test_get_year_bad2(self):
        finder = FriendFinder()
        actual_year = finder.get_year("1.1111")
        expected = np.nan
        assert (actual_year == expected)

    def test_get_year_bad3(self):
        finder = FriendFinder()
        actual_year = finder.get_year(1111)
        assert (np.isnan(actual_year))

    def test_is_same_city(self):
        finder = FriendFinder()


    def test_get_lvl_by_id(self):
        self.fail()

    def test_generate(self):
        self.fail()
