import os
import unittest

from src import ingestion

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestIngestion(unittest.TestCase):

    def test_read_csv_as_dataframes(self):
        test_input = f"{ROOT_PATH}/data/dummy_fleet.csv"
        actual = ingestion.read_csv_as_dataframes(test_input)
        self.assertEqual(actual.shape, (5, 5))
        self.assertEqual(actual.size, 5 * 5)


if __name__ == '__main__':
    unittest.main()
