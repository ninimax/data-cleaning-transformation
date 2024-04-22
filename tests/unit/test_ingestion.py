import unittest

from src import ingestion


class TestIngestion(unittest.TestCase):

    def test_count_duplicates(self):
        test_input = "../data/maintenance_records.csv"
        actual = ingestion.read_as_dataframes(test_input)
        expected = 2
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
