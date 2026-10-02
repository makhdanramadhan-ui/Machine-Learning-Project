"""Regresi input invalid, konsistensi probabilitas, dan alur Streamlit nyata."""
import io
import json
import logging
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import joblib
import numpy as np
import pandas as pd
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from calibrate import classification_metrics
from prediction import (
    InputValidationError, example_customers, input_schema,
    predict_customers, risk_levels, validate_input,
)
from training_data import load_training_split


class PredictionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipe = joblib.load(ROOT / "model_churn.pkl")
        cls.cal = joblib.load(ROOT / "calibrator.pkl")
        cls.schema = input_schema(cls.pipe)
        cls.info = json.loads((ROOT / "deployment_info.json").read_text(encoding="utf-8"))
        cls.threshold = cls.info["threshold"]

    def test_raw_dataset_and_template_are_accepted(self):
        raw = pd.read_csv(ROOT / "Telco-Customer-Churn.csv")
        self.assertEqual(len(validate_input(raw, self.schema)), 7043)
        self.assertEqual(len(validate_input(example_customers(), self.schema)), 2)

    def test_invalid_inputs_are_reported_without_prediction(self):
        frame = example_customers()
        invalid = [
            (frame.iloc[:0], "belum berisi"),
            (frame.drop(columns="tenure"), "tenure"),
            (frame.assign(MonthlyCharges=np.nan), "MonthlyCharges"),
            (frame.assign(MonthlyCharges=np.inf), "berhingga"),
            (frame.assign(MonthlyCharges="abc"), "MonthlyCharges"),
            (frame.assign(MonthlyCharges=-1), "0 dan 120"),
            (frame.assign(tenure=2.5), "bulan bulat"),
            (frame.assign(SeniorCitizen=2), "0 atau 1"),
            (frame.assign(Contract="Two years"), "Contract"),
            (frame.assign(PhoneService=None), "PhoneService"),
            (frame.assign(InternetService=None), "InternetService"),
            (frame.assign(OnlineSecurity="No internet service"), "DSL/Fiber"),
            (frame.assign(InternetService="No"), "InternetService=No"),
            (frame.assign(MultipleLines="No phone service"), "PhoneService=Yes"),
        ]
        for data, message in invalid:
            with self.subTest(message=message):
                with self.assertRaisesRegex(InputValidationError, message):
                    predict_customers(data, self.cal, self.schema, self.threshold)

    def test_holdout_predictions_match_deployment_metadata(self):
        _, X_test, _, y_test = load_training_split()
        probabilities, labels = predict_customers(X_test, self.cal, self.schema, self.threshold)
        self.assertEqual(classification_metrics(y_test, probabilities, self.threshold), self.info["metrics"])
        np.testing.assert_array_equal(labels, probabilities >= self.threshold)
        self.assertFalse(((labels == 1) & (risk_levels(probabilities, self.threshold) == "RENDAH")).any())

    def test_decision_boundary_and_whitespace(self):
        class BoundaryModel:
            classes_ = np.array([0, 1])

            def predict_proba(inner_self, data):
                probs = np.array([self.threshold - 0.00001, self.threshold])
                return np.column_stack([1 - probs, probs])

        frame = example_customers().assign(Contract=[" Month-to-month ", " Two year "])
        _, labels = predict_customers(frame, BoundaryModel(), self.schema, self.threshold)
        np.testing.assert_array_equal(labels, [0, 1])


class StreamlitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    def run_app(self):
        at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()
        self.assertEqual([x.message for x in at.exception], [])
        return at

    def test_form_services_and_stale_result(self):
        at = self.run_app()
        public_text = "\n".join(x.value for x in at.markdown) + "\n" + "\n".join(x.value for x in at.caption)
        self.assertNotIn("NASKAH_VIDEO", public_text)
        self.assertNotIn("Naskah video", public_text)
        self.assertNotIn("cohort", public_text.lower())
        self.assertIn("pelanggan setelah data dibersihkan", public_text)
        self.assertTrue(any("Arti" in x.value.columns for x in at.dataframe))
        at.button[0].click().run()
        self.assertEqual([x.message for x in at.exception], [])
        self.assertTrue(any("Keputusan model:" in x.value for x in at.markdown))
        at.number_input[0].set_value(24).run()
        self.assertFalse(any("Keputusan model:" in x.value for x in at.markdown))
        self.assertTrue(any("Input telah berubah" in x.value for x in at.info))
        at.selectbox[6].select("No").run()
        for widget in at.selectbox[7:13]:
            self.assertEqual(widget.value, "No internet service")
            self.assertTrue(widget.disabled)
        at.selectbox[6].select("DSL").run()
        for widget in at.selectbox[7:13]:
            self.assertNotIn("No internet service", widget.options)
        at.selectbox[4].select("No").run()
        self.assertEqual(at.selectbox[5].value, "No phone service")
        at.selectbox[4].select("Yes").run()
        self.assertNotIn("No phone service", at.selectbox[5].options)
        at.button[0].click().run()
        self.assertEqual([x.message for x in at.exception], [])

    def test_batch_results_and_invalid_csv_feedback(self):
        valid = example_customers().to_csv(index=False).encode()
        invalid_column = example_customers().drop(columns="tenure").to_csv(index=False).encode()
        invalid_number = example_customers().assign(MonthlyCharges=np.nan).to_csv(index=False).encode()
        invalid_category = example_customers().assign(Contract="Two years").to_csv(index=False).encode()
        duplicate_header = valid.replace(b"gender,SeniorCitizen", b"gender,gender", 1)
        cases = [(valid, True), (invalid_column, False), (invalid_number, False),
                 (invalid_category, False), (duplicate_header, False),
                 (b"", False), (b"a,b\n\"unfinished", False), (b"\xff", False)]
        for payload, expected_valid in cases:
            with self.subTest(valid=expected_valid, payload=payload[:40]):
                upload = io.BytesIO(payload)
                upload.name = "test.csv"
                with patch("streamlit.file_uploader", return_value=upload):
                    at = self.run_app()
                outputs = [x.value for x in at.dataframe if "Prediksi" in x.value.columns]
                if expected_valid:
                    self.assertEqual(len(outputs), 1)
                    self.assertEqual(len(outputs[0]), 2)
                    self.assertIn("Threshold_Churn", outputs[0].columns)
                    self.assertFalse(((outputs[0]["Prediksi"] == "CHURN") &
                                      (outputs[0]["Risiko"] == "RENDAH")).any())
                    self.assertFalse(at.error)
                else:
                    self.assertFalse(outputs)
                    self.assertTrue(at.error)


if __name__ == "__main__":
    unittest.main()
