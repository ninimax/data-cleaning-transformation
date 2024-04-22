import unittest

import pandas as pd

from src import quality_checks


class TestQualityChecks(unittest.TestCase):

    def test_count_duplicates(self):
        test_input = pd.DataFrame({"name": ["A", "B", "B", "B", "C"], "id": [1, 2, 2, 22, 3]})
        actual = quality_checks.count_full_duplicates(test_input)
        expected = 2
        self.assertEqual(expected, actual)

    def test_count_missing_val_per_col(self):
        test_input = pd.DataFrame({"name": ["A", pd.NA, pd.NA, pd.NA, "C"], "id": [1, 2, 2, pd.NA, 3]})
        actual = quality_checks.count_missing_val_per_col(test_input)
        expected = pd.Series({"name": 3, "id": 1})
        self.assertEqual(expected["name"], actual["name"])
        self.assertEqual(expected["id"], actual["id"])

    def test_get_items_existing_in_df1_only(self):
        test_input_1 = pd.DataFrame({"name": ["A", "B", "B", "B", "C"], "id": [1, 2, 2, 22, 3]})
        test_input_2 = pd.DataFrame({"name": ["A", "B", "B", "B", "C"], "id": [1, 2, 2, 33, 3]})
        actual = quality_checks.get_items_existing_in_df1_only(test_input_1, test_input_2, "id")
        expected = [22]
        self.assertEqual(expected, actual)

    def test_validate_email_pass(self):
        test_input = "a@b.c"
        actual = quality_checks.validate_email(test_input)
        expected = True
        self.assertEqual(expected, actual)

    def test_validate_email_fail(self):
        test_input = "ab.c"
        actual = quality_checks.validate_email(test_input)
        expected = False
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
