import os
import unittest

import pandas as pd

from src import pipeline

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestPipeline(unittest.TestCase):

    def test_run(self):
        export_file_path = f"{ROOT_PATH}/data/dummy_export.csv"
        pipeline.run(
            f"{ROOT_PATH}/data/dummy_fleet.csv",
            f"{ROOT_PATH}/data/dummy_maintenance.csv",
            export_file_path)

        try:
            exported_df = pd.read_csv(export_file_path)
        except Exception as e:
            raise AssertionError(f"Export file should be found, but: {e}")

        # NOTE! While exporting pandas DataFrame to csv,
        # NaTs are automatically converted to NaNs to support csv.
        self.assertEqual("DUMMY001", exported_df["truck_id"][0])
        self.assertEqual("nan", str(exported_df["purchase_date"][0]))
        self.assertEqual(False, exported_df["service_type_inspection"][0])
        self.assertEqual(False, exported_df["service_type_maintenance"][0])
        self.assertEqual(True, exported_df["service_type_repair"][0])
        self.assertEqual(False, exported_df["email_valid"][0])

        self.assertEqual("DUMMY002", exported_df["truck_id"][1])
        self.assertEqual(pd.to_datetime("29-07-2023"),
                         pd.to_datetime(exported_df["purchase_date"][1]))
        self.assertEqual(True, exported_df["service_type_inspection"][1])
        self.assertEqual(False, exported_df["service_type_maintenance"][1])
        self.assertEqual(False, exported_df["service_type_repair"][1])
        self.assertEqual(True, exported_df["email_valid"][1])

        self.assertEqual("DUMMY003", exported_df["truck_id"][2])
        self.assertEqual("nan", str(exported_df["purchase_date"][2]))
        self.assertEqual(True, exported_df["service_type_inspection"][2])
        self.assertEqual(False, exported_df["service_type_maintenance"][2])
        self.assertEqual(False, exported_df["service_type_repair"][2])
        self.assertEqual(False, exported_df["email_valid"][2])

        self.assertEqual("DUMMY003", exported_df["truck_id"][3])
        self.assertEqual("nan", str(exported_df["purchase_date"][3]))
        self.assertEqual(False, exported_df["service_type_inspection"][3])
        self.assertEqual(True, exported_df["service_type_maintenance"][3])
        self.assertEqual(False, exported_df["service_type_repair"][3])
        self.assertEqual(False, exported_df["email_valid"][3])


if __name__ == "__main__":
    unittest.main()
