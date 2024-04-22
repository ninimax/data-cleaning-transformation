import os
import unittest

from src import ingestion

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestIngestion(unittest.TestCase):

    def test_read_as_dataframes(self):
        test_input = f"{ROOT_PATH}/data/dummy_data.csv"
        actual = ingestion.read_as_dataframes(test_input)
        self.assertEqual(actual.shape, (4, 5))
        self.assertEqual(actual.size, 4 * 5)


if __name__ == '__main__':
    unittest.main()
