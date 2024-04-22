import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from src import processing


class TestProcessing(unittest.TestCase):

    def test_merge(self):
        test_input_1 = pd.DataFrame({"Name": ["A", "B", "BB", "C"], "ID": [1, 2, 22, 3]})
        test_input_2 = pd.DataFrame({"Description": ["desc_A", "desc_B", "desc_CC", "desc_C"], "ID": [1, 2, 33, 3]})
        actual = processing.merge(test_input_1, test_input_2, "ID")
        expected = pd.DataFrame(
            {"Name": ["A", "B", "C"], "ID": [1, 2, 3], "Description": ["desc_A", "desc_B", "desc_C"]}
        )

        assert_frame_equal(expected, actual)

    def test_standardize_text(self):
        test_input = pd.DataFrame({"Name": [" A", "B ", "BB", " C "], "ID": [1, 2, 22, 3]})
        actual = processing.standardize_text(test_input, "Name")
        expected = pd.DataFrame({"Name": ["a", "b", "bb", "c"], "ID": [1, 2, 22, 3]})
        assert_frame_equal(expected, actual)

    def test_standardize_dates(self):
        test_input = pd.DataFrame({"Dates": ["2001-01-01", "02-02-2022", "03-2023/03", "04/04/2024", "1999.09.09"]})
        actual = processing.standardize_dates(test_input, "Dates")
        expected = pd.DataFrame({"Dates": [pd.NaT, pd.to_datetime("02-02-2022"), pd.NaT, pd.NaT, pd.NaT]})
        assert_frame_equal(expected, actual)

    def test_encode_one_hot(self):
        test_input = pd.DataFrame({"Types": ["Maintenance", "Inspection", pd.NA, "Inspection", "Repair"],
                                   "ID": [1, 2, 3, 4, 5]
                                   })
        actual = processing.encode_one_hot(test_input, "Types")
        expected = pd.DataFrame({"Types": ["Maintenance", "Inspection", pd.NA, "Inspection", "Repair"],
                                 "ID": [1, 2, 3, 4, 5],
                                 "Inspection": [False, True, False, True, False],
                                 "Maintenance": [True, False, False, False, False],
                                 "Repair": [False, False, False, False, True]
                                 })
        assert_frame_equal(expected, actual)


if __name__ == "__main__":
    unittest.main()
