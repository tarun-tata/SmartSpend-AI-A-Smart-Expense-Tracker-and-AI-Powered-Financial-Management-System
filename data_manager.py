import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self, csv_file="expenses.csv"):
        self.csv_file = csv_file

    def load_data(self):
        if not os.path.exists(self.csv_file):
            logger.info("CSV file not found, returning empty DataFrame.")
            return pd.DataFrame(columns=["Date", "Type", "Category", "Description", "Amount"])
        try:
            df = pd.read_csv(self.csv_file)
            logger.info(f"Successfully loaded {len(df)} records.")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def save_record(self, record):
        try:
            df_new = pd.DataFrame([record])
            if os.path.exists(self.csv_file):
                df_existing = pd.read_csv(self.csv_file)
                df_all = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_all = df_new
            df_all.to_csv(self.csv_file, index=False)
            logger.info(f"Saved new record: {record['Description']}")
        except Exception as e:
            logger.error(f"Error saving record: {e}")
            raise

    def get_summary(self):
        df = self.load_data()
        if df.empty:
            return None
        
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
        total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
        total_income = df[df["Type"] == "Income"]["Amount"].sum()
        
        by_category = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum().to_dict()
        
        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "net_balance": float(total_income - total_expense),
            "by_category": by_category
        }
