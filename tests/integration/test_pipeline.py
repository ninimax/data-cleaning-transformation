import unittest

from src import pipeline


class TestPipeline(unittest.TestCase):

    def test_count_duplicates(self):
        actual = pipeline.run()
        expected = True
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
