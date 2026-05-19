import unittest
import os
import pandas as pd
from data_manager import DataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.test_csv = "test_expenses.csv"
        self.dm = DataManager(self.test_csv)

    def tearDown(self):
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)

    def test_save_and_load(self):
        record = {
            "Date": "2024-05-19",
            "Type": "Expense",
            "Category": "Food",
            "Description": "Test Pizza",
            "Amount": 15.50
        }
        self.dm.save_record(record)
        df = self.dm.load_data()
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Description"], "Test Pizza")

    def test_summary(self):
        records = [
            {"Date": "2024-05-19", "Type": "Expense", "Category": "Food", "Description": "A", "Amount": 10},
            {"Date": "2024-05-19", "Type": "Income", "Category": "Other", "Description": "B", "Amount": 100}
        ]
        for r in records:
            self.dm.save_record(r)
        
        summary = self.dm.get_summary()
        self.assertEqual(summary["total_income"], 100)
        self.assertEqual(summary["total_expense"], 10)
        self.assertEqual(summary["net_balance"], 90)

    def test_ai_suggestion_fallback(self):
        from ai_helper import AIHelper
        helper = AIHelper()
        categories = ["Food", "Travel", "Bills", "Shopping", "Entertainment", "Health", "Other"]
        
        # Test keyword matching
        self.assertEqual(helper.suggest_category("Bought some chips", categories), "Food")
        self.assertEqual(helper.suggest_category("Trip to Germany", categories), "Travel")
        self.assertEqual(helper.suggest_category("Electric bill", categories), "Bills")
        self.assertEqual(helper.suggest_category("New shoes", categories), "Shopping")
        self.assertEqual(helper.suggest_category("Random stuff", categories), "Other")

if __name__ == "__main__":
    unittest.main()
