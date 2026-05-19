import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
from data_manager import DataManager
from ai_helper import AIHelper

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CATEGORIES = ["Food", "Travel", "Bills", "Shopping", "Entertainment", "Health", "Other"]

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartSpend AI")
        self.root.geometry("1000x700")
        
        # Initialize modules
        self.data_manager = DataManager()
        self.ai_helper = AIHelper()
        
        self.setup_styles()
        self.create_widgets()
        self.refresh_table()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam') # More modern than default
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        style.configure("TButton", padding=5)
        style.configure("Action.TButton", foreground="blue")

    def create_widgets(self):
        # Main Container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)

        # --------- Top Form Frame ---------
        form_frame = ttk.LabelFrame(main_frame, text=" Add New Transaction ", padding="10")
        form_frame.pack(fill="x", pady=(0, 10))

        # Row 0: Date and Category
        ttk.Label(form_frame, text="Date:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.date_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
        ttk.Entry(form_frame, textvariable=self.date_var, width=15).grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(form_frame, text="Category:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=CATEGORIES, width=15, state="readonly")
        self.category_combo.grid(row=0, column=3, sticky="w", padx=5)
        self.category_combo.current(0)

        # AI Suggest Button
        ai_suggest_btn = ttk.Button(form_frame, text="✨ AI Suggest Category", command=self.ai_suggest_category)
        ai_suggest_btn.grid(row=0, column=4, padx=10)

        # Row 1: Description and Amount
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.desc_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.desc_var, width=40).grid(row=1, column=1, columnspan=2, sticky="w", padx=5)

        ttk.Label(form_frame, text="Amount:").grid(row=1, column=3, sticky="e", padx=5, pady=5)
        self.amount_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.amount_var, width=10).grid(row=1, column=4, sticky="w", padx=5)

        # Row 2: Type and Actions
        type_frame = ttk.Frame(form_frame)
        type_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")
        self.type_var = tk.StringVar(value="Expense")
        ttk.Radiobutton(type_frame, text="Expense", variable=self.type_var, value="Expense").pack(side="left", padx=5)
        ttk.Radiobutton(type_frame, text="Income", variable=self.type_var, value="Income").pack(side="left", padx=5)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=2, columnspan=3, sticky="e")
        
        ttk.Button(btn_frame, text="Add Transaction", style="Action.TButton", command=self.add_transaction).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=5)

        # --------- Middle: Dashboard/Actions ---------
        dash_frame = ttk.Frame(main_frame, padding="5")
        dash_frame.pack(fill="x", pady=5)

        ttk.Button(dash_frame, text="📊 Show Summary", command=self.show_summary).pack(side="left", padx=5)
        ttk.Button(dash_frame, text="📈 View Chart", command=self.show_chart).pack(side="left", padx=5)
        ttk.Button(dash_frame, text="🤖 Get AI Financial Advice", command=self.get_ai_advice).pack(side="left", padx=5)
        ttk.Button(dash_frame, text="🔄 Refresh", command=self.refresh_table).pack(side="right", padx=5)

        # --------- Bottom: Table ---------
        table_frame = ttk.LabelFrame(main_frame, text=" Transaction History ", padding="5")
        table_frame.pack(fill="both", expand=True)

        columns = ("date", "type", "category", "description", "amount")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("date", text="Date")
        self.tree.heading("type", text="Type")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.heading("amount", text="Amount")

        self.tree.column("date", width=100)
        self.tree.column("type", width=80)
        self.tree.column("category", width=120)
        self.tree.column("description", width=400)
        self.tree.column("amount", width=100, anchor="e")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def ai_suggest_category(self):
        desc = self.desc_var.get().strip()
        if not desc:
            messagebox.showwarning("AI Suggest", "Please enter a description first.")
            return
        
        suggested = self.ai_helper.suggest_category(desc, CATEGORIES)
        self.category_var.set(suggested)
        logger.info(f"AI suggested category '{suggested}' for description '{desc}'")

    def get_ai_advice(self):
        summary = self.data_manager.get_summary()
        if not summary:
            messagebox.showinfo("AI Advice", "Add some transactions first to get advice!")
            return
        
        advice = self.ai_helper.get_financial_advice(summary)
        messagebox.showinfo("AI Financial Advisor", advice)

    def add_transaction(self):
        try:
            date_str = self.date_var.get().strip()
            tx_type = self.type_var.get()
            category = self.category_var.get()
            desc = self.desc_var.get().strip()
            amount_str = self.amount_var.get().strip()

            if not desc or not amount_str:
                raise ValueError("Description and Amount are required.")

            amount = float(amount_str)
            datetime.strptime(date_str, "%Y-%m-%d") # Validate date format

            record = {
                "Date": date_str,
                "Type": tx_type,
                "Category": category,
                "Description": desc,
                "Amount": amount
            }

            self.data_manager.save_record(record)
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Success", "Transaction added successfully.")
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            logger.error(f"Error adding transaction: {e}")
            messagebox.showerror("Error", "An unexpected error occurred.")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        df = self.data_manager.load_data()
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(
                row["Date"],
                row["Type"],
                row["Category"],
                row["Description"],
                f"{float(row['Amount']):.2f}"
            ))

    def show_summary(self):
        summary = self.data_manager.get_summary()
        if not summary:
            messagebox.showinfo("Summary", "No data available.")
            return

        text = f"Total Income: {summary['total_income']:.2f}\n"
        text += f"Total Expense: {summary['total_expense']:.2f}\n"
        text += f"Net Balance: {summary['net_balance']:.2f}\n\n"
        text += "Expenses by Category:\n"
        for cat, amt in summary['by_category'].items():
            text += f"  {cat}: {amt:.2f}\n"
        
        messagebox.showinfo("Financial Summary", text)

    def show_chart(self):
        import matplotlib.pyplot as plt
        df = self.data_manager.load_data()
        exp_df = df[df["Type"] == "Expense"]
        if exp_df.empty:
            messagebox.showinfo("Chart", "No expenses to display.")
            return
        
        by_cat = exp_df.groupby("Category")["Amount"].sum()
        plt.figure(figsize=(8, 6))
        by_cat.plot(kind='pie', autopct='%1.1f%%', startangle=140)
        plt.title("Expenses by Category")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()

    def clear_form(self):
        self.desc_var.set("")
        self.amount_var.set("")
        self.date_var.set(datetime.today().strftime("%Y-%m-%d"))
        self.category_combo.current(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
