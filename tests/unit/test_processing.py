import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from src import processing


class TestProcessing(unittest.TestCase):

    def test_merge(self):
        test_input_1 = pd.DataFrame(
            {
                "name": ["a", "b", "bb", "c"],
                "id": [1, 2, 22, 3]
            })
        test_input_2 = pd.DataFrame(
            {
                "description": ["desc_a", "desc_b", "desc_cc", "desc_c"],
                "id": [1, 2, 33, 3]
            })
        actual = processing.merge(test_input_1, test_input_2, "id")
        expected = pd.DataFrame(
            {
                "name": ["a", "b", "c"], "id": [1, 2, 3],
                "description": ["desc_a", "desc_b", "desc_c"]
            }
        )

        assert_frame_equal(expected, actual)

    def test_standardize_text(self):
        test_input = pd.DataFrame(
            {
                "name": [" A", "B ", "BB", " C "],
                "id": [1, 2, 22, 3]
            })
        actual = processing.standardize_text(test_input, "name")
        expected = pd.DataFrame(
            {
                "name": ["a", "b", "bb", "c"],
                "id": [1, 2, 22, 3]
            })
        assert_frame_equal(expected, actual)

    def test_standardize_dates(self):
        test_input = pd.DataFrame(
            {
                "dates": ["2001-01-01",
                          "02-02-2022",
                          "03-2023/03",
                          "04/04/2024",
                          "1999.09.09"]
            })
        actual = processing.standardize_dates(test_input, "dates")
        expected = pd.DataFrame(
            {
                "dates": [pd.NaT,
                          pd.to_datetime("02-02-2022"),
                          pd.NaT,
                          pd.NaT,
                          pd.NaT]
            })
        assert_frame_equal(expected, actual)

    def test_encode_one_hot(self):
        test_input = pd.DataFrame(
            {
                "type": [
                    "maintenance",
                    "inspection",
                    pd.NA,
                    "inspection",
                    "repair"],
                "id": [1, 2, 3, 4, 5]
            })
        actual = processing.encode_one_hot(test_input, "type")
        expected = pd.DataFrame(
            {
                "id": [1, 2, 3, 4, 5],
                "inspection": [False, True, False, True, False],
                "maintenance": [True, False, False, False, False],
                "repair": [False, False, False, False, True]
            })
        assert_frame_equal(expected, actual)

    def test_add_column_email_valid(self):
        test_input = pd.DataFrame(
            {
                "email": ["a/b.com", "a@b.c", "123", "aa@bb.cc", "blabla"],
                "id": [1, 2, 3, 4, 5]
            })
        actual = processing.add_column_email_valid(test_input, "email")
        expected = pd.DataFrame(
            {
                "email": ["a/b.com", "a@b.c", "123", "aa@bb.cc", "blabla"],
                "id": [1, 2, 3, 4, 5],
                "email_valid": [False, True, False, True, False]
            })
        assert_frame_equal(expected, actual)


if __name__ == "__main__":
    unittest.main()
