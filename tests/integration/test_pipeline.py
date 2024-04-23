import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from src import pipeline


class TestPipeline(unittest.TestCase):

    def test_run(self):
        export_file_path = "../data/export.csv"
        pipeline.run(
            "../data/dummy_fleet.csv",
            "../data/dummy_maintenance.csv",
            "../data/export.csv")

        exported_df = None

        try:
            exported_df = pd.read_csv(export_file_path)
        except Exception as e:
            raise AssertionError(f"Export file should be found, but: {e}")

        self.assertEqual("DUMMY001", exported_df["truck_id"][0])
        #self.assertEqual(pd.NaT, exported_df["purchase_date"][0])
        self.assertEqual(False, exported_df["service_type_inspection"][0])
        self.assertEqual(False, exported_df["service_type_maintenance"][0])
        self.assertEqual(True, exported_df["service_type_repair"][0])
        self.assertEqual(False, exported_df["email_valid"][0])

        self.assertEqual("DUMMY002", exported_df["truck_id"][1])
        #self.assertEqual(pd.NaT, exported_df["purchase_date"][1])
        self.assertEqual(True, exported_df["service_type_inspection"][1])
        self.assertEqual(False, exported_df["service_type_maintenance"][1])
        self.assertEqual(False, exported_df["service_type_repair"][1])
        self.assertEqual(True, exported_df["email_valid"][1])

        self.assertEqual("DUMMY003", exported_df["truck_id"][2])
        #self.assertEqual(pd.NaT, exported_df["purchase_date"][2])
        self.assertEqual(True, exported_df["service_type_inspection"][2])
        self.assertEqual(False, exported_df["service_type_maintenance"][2])
        self.assertEqual(False, exported_df["service_type_repair"][2])
        self.assertEqual(False, exported_df["email_valid"][2])

        self.assertEqual("DUMMY003", exported_df["truck_id"][3])
        #self.assertEqual(pd.NaT, exported_df["purchase_date"][3])
        self.assertEqual(False, exported_df["service_type_inspection"][3])
        self.assertEqual(True, exported_df["service_type_maintenance"][3])
        self.assertEqual(False, exported_df["service_type_repair"][3])
        self.assertEqual(False, exported_df["email_valid"][3])

if __name__ == "__main__":
    unittest.main()
