import unittest

import pandas as pd

from src import quality_checks


class TestQualityChecks(unittest.TestCase):

    def test_count_duplicates(self):
        test_input = pd.DataFrame({'Name': ['A', 'B', 'B', 'B', 'C'], 'ID': [1, 2, 2, 22, 3]})
        actual = quality_checks.count_full_duplicates(test_input)
        expected = 2
        self.assertEqual(expected, actual)

    def test_count_missing_val_per_col(self):
        test_input = pd.DataFrame({'Name': ['A', pd.NA, pd.NA, pd.NA, 'C'], 'ID': [1, 2, 2, pd.NA, 3]})
        actual = quality_checks.count_missing_val_per_col(test_input)
        expected = pd.Series({"Name": 3, "ID": 1})
        self.assertEqual(expected["Name"], actual["Name"])
        self.assertEqual(expected["ID"], actual["ID"])

    def test_get_id_existing_in_df1_only(self):
        test_input = pd.DataFrame({'Name': ['A', 'B', 'B', 'B', 'C'], 'ID': [1, 2, 2, 22, 3]})
        actual = quality_checks.get_id_existing_in_df1_only(test_input, test_input)
        expected = 2
        self.assertEqual(expected, actual)

    def test_validate_email_pass(self):
        test_input = 'a@b.c'
        actual = quality_checks.validate_email(test_input)
        expected = True
        self.assertEqual(expected, actual)

    def test_validate_email_fail(self):
        test_input = 'ab.c'
        actual = quality_checks.validate_email(test_input)
        expected = False
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
