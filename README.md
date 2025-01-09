# Expense Tracker

## Overview
The **Expense Tracker** is a user-friendly and interactive web application developed using Streamlit. It enables users to manage their personal finances effectively by tracking expenses, setting budgets, analyzing spending trends, and generating financial reports. This tool is perfect for individuals looking to gain insights into their spending habits and take control of their finances.

## Features
1. **Dashboard**:
   - View total expenses, monthly average, and predicted expenses for the next month.
   - Visualize spending trends with a 7-day rolling average.
   - Analyze category-wise spending through pie charts.
   - Get smart insights into your spending habits and review recent transactions.

2. **Add Expense**:
   - Add new expenses with details such as description, amount, category, and date.

3. **View Expenses**:
   - Display all recorded expenses in a tabular format.
   - Export expenses as a CSV file for offline use.

4. **Update/Delete Expense**:
   - Update existing expense details.
   - Delete unwanted expense records.

5. **Budget Management**:
   - Set monthly budgets for different months.
   - Check budget status to see if you're within the limit or have exceeded it.

6. **Analytics**:
   - Visualize monthly spending trends with line charts.
   - Analyze category-wise expense breakdown.
   - Get metrics such as total expenses, average expense, and highest expense.

7. **Reports**:
   - Generate a detailed financial report as a PDF.
   - Includes charts, category breakdowns, and transaction details.

## Installation
To run the app locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/NotIshi28/expense-tracker.git
   cd expense-tracker
   ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the App**:
   ```bash
   streamlit run app.py
   ```
   The app will open in your default web browser at `http://localhost:8501/`.

## Usage
1. **Start the App**: Launch the app by running the `streamlit run app.py` command.
2. **Navigate**: Use the sidebar to navigate between different pages (Dashboard, Add Expense, Analytics, etc.).
3. **Add Data**: Enter your expenses and budgets using the provided forms.
4. **Analyze**: Visualize your spending patterns and get actionable insights.
5. **Export Data**: Generate PDF reports to share or archive your financial records.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with descriptions of your changes.