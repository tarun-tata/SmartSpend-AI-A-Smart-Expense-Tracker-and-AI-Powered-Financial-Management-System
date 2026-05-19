# SmartSpend AI

A professional and operational expense tracking application built with Python and Tkinter, featuring AI-powered insights and category suggestions.

## Features

- **Transaction Management**: Add and track income and expenses.
- **AI Category Suggestion**: Uses AI (or keyword matching fallback) to automatically suggest categories based on descriptions.
- **AI Financial Advisor**: Get personalized financial advice based on your spending patterns.
- **Visual Analytics**: Interactive pie charts showing expense distribution by category.
- **Operational Excellence**:
  - Modular code structure (`data_manager.py`, `ai_helper.py`).
  - Comprehensive logging (`app.log`).
  - Error handling and data validation.
  - Environment variable support for API keys.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "Smart Expense Tracker"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AI (Optional)**:
   - Copy `.env.example` to `.env`.
   - Add your `OPENAI_API_KEY` to the `.env` file for full AI capabilities.
   - If no key is provided, the app will use a smart rule-based fallback.

4. **Run the application**:
   ```bash
   python expense.py
   ```

## Project Structure

- `expense.py`: Main application entry point and UI logic.
- `data_manager.py`: Handles CSV data operations and summary calculations.
- `ai_helper.py`: AI integration for suggestions and advice.
- `expenses.csv`: Local data storage.
- `app.log`: Application runtime logs.
- `requirements.txt`: Project dependencies.

## Contributing

Feel free to fork and submit pull requests!
