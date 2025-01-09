import streamlit as st
import json
import csv
from datetime import datetime
import pandas as pd
import plotly.express as px
import calendar
from fpdf import FPDF
import matplotlib.pyplot as plt
import os


st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'expenses' not in st.session_state:
    st.session_state.expenses = []

if 'budgets' not in st.session_state:
    st.session_state.budgets = {}


def load_expenses():
    return st.session_state.expenses

def save_expenses(expenses):
    st.session_state.expenses = expenses

def load_budgets():
    return st.session_state.budgets

def save_budgets(budgets):
    st.session_state.budgets = budgets

def calculate_trends(expenses_df):
    if not expenses_df.empty:
        expenses_df['date'] = pd.to_datetime(expenses_df['date'])
        daily_expenses = expenses_df.groupby('date')['amount'].sum()
        trend = daily_expenses.rolling(window=7).mean()
        return trend
    return pd.Series()

def predict_future_expenses(expenses_df):
    if not expenses_df.empty:
        expenses_df['date'] = pd.to_datetime(expenses_df['date'])
        monthly_expenses = expenses_df.groupby(pd.Grouper(key='date', freq='ME'))['amount'].sum()
        prediction = monthly_expenses.mean()
        return prediction
    return 0

def get_spending_insights(expenses_df):
    if not expenses_df.empty:
        insights = []
        
        top_category = expenses_df.groupby('category')['amount'].sum().idxmax()
        insights.append(f"Your highest spending category is {top_category}")
        
        daily_avg = expenses_df.groupby('date')['amount'].sum().mean()
        insights.append(f"Your daily average spending is ${daily_avg:.2f}")
        
        weekday_spending = expenses_df.groupby(pd.to_datetime(expenses_df['date']).dt.dayofweek)['amount'].mean()
        highest_day = calendar.day_name[weekday_spending.idxmax()]
        insights.append(f"You tend to spend more on {highest_day}s")
        
        return insights
    return []

def export_to_pdf(expenses_df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16, style='B')
    pdf.set_text_color(33, 150, 243)
    pdf.cell(200, 10, txt="Expense Tracker Report", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    if not expenses_df.empty:
        
        total_expenses = expenses_df['amount'].sum()
        avg_expense = expenses_df['amount'].mean()
        highest_expense = expenses_df['amount'].max()
        highest_category = expenses_df.groupby('category')['amount'].sum().idxmax()

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Total Expenses: ${total_expenses:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Average Expense: ${avg_expense:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Highest Expense: ${highest_expense:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Most Expensive Category: {highest_category}", ln=True)
        pdf.ln(10)

        category_totals = expenses_df.groupby('category')['amount'].sum()
        category_totals.plot(kind='bar', color='skyblue')
        plt.title("Category-wise Expenses")
        plt.ylabel("Amount ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        bar_chart_path = "category_breakdown.png"
        plt.savefig(bar_chart_path)
        plt.close()

        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(200, 10, txt="Category Breakdown (Chart):", ln=True)
        pdf.image(bar_chart_path, x=10, y=None, w=190)
        pdf.ln(80)

        category_totals.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        plt.title("Expense Distribution")
        plt.ylabel("")  
        pie_chart_path = "expense_distribution.png"
        plt.savefig(pie_chart_path)
        plt.close()
        
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(200, 10, txt="Expense Distribution (Chart):", ln=True)
        pdf.image(pie_chart_path, x=10, y=None, w=190)
        pdf.ln(80)
        
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(200, 10, txt="Detailed Transactions:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.set_fill_color(240, 240, 240)
        for idx, row in expenses_df.iterrows():
            pdf.cell(0, 10, txt=f"{row['date']} - {row['category']} - ${row['amount']:.2f} ({row['description']})", ln=True, fill=(idx % 2 == 0))
        pdf.ln(10)
        
        os.remove(bar_chart_path)
        os.remove(pie_chart_path)

    else:
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="No expenses recorded.", ln=True)
    
    pdf.set_y(-15)
    pdf.set_font("Arial", size=10, style='I')
    pdf.cell(0, 10, txt="Generated using Expense Tracker", align='C')

    pdf.output("Expense_Report.pdf")
    return "Expense_Report.pdf"

def main():
    
    with st.sidebar:
        st.title("Expense Tracker")
        
        
        with st.expander("📤 Data Management", expanded=False):
            expenses_file = st.file_uploader("Upload Expenses JSON", type=['json'])
            if expenses_file is not None:
                try:
                    st.session_state.expenses = json.load(expenses_file)
                    st.success("Expenses loaded successfully!")
                except Exception as e:
                    st.error(f"Error loading expenses: {str(e)}")

            budgets_file = st.file_uploader("Upload Budgets JSON", type=['json'])
            if budgets_file is not None:
                try:
                    st.session_state.budgets = json.load(budgets_file)
                    st.success("Budgets loaded successfully!")
                except Exception as e:
                    st.error(f"Error loading budgets: {str(e)}")

    
    page = st.sidebar.radio(
        "Navigation",
        ["📊 Dashboard", "➕ Add Expense", "📋 View Expenses", "✏️ Update/Delete", "💰 Budget Management", "📈 Analytics", "📄 Reports"]
    )

    if page == "📊 Dashboard":
        st.title("Financial Dashboard")
        
        
        col1, col2, col3, col4 = st.columns(4)
        expenses = load_expenses()
        if expenses:
            df = pd.DataFrame(expenses)
            df['date'] = pd.to_datetime(df['date'])
            
            with col1:
                st.metric("Total Expenses", f"${df['amount'].sum():,.2f}")
            with col2:
                monthly_avg = df.groupby(df['date'].dt.strftime('%Y-%m'))['amount'].sum().mean()
                st.metric("Monthly Average", f"${monthly_avg:,.2f}")
            with col3:
                today = datetime.now()
                month_expenses = df[df['date'].dt.month == today.month]['amount'].sum()
                st.metric("This Month", f"${month_expenses:,.2f}")
            with col4:
                prediction = predict_future_expenses(df)
                st.metric("Next Month (Predicted)", f"${prediction:,.2f}")

        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Expense Trends")
            if expenses:
                trend = calculate_trends(df)
                fig = px.line(trend, title="7-Day Rolling Average")
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Category Distribution")
            if expenses:
                fig = px.pie(df, values='amount', names='category', hole=0.4)
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("💡 Smart Insights")
            if expenses:
                insights = get_spending_insights(df)
                for insight in insights:
                    st.info(insight)

        with col2:
            st.subheader("Recent Transactions")
            if expenses:
                recent = df.sort_values('date', ascending=False).head(5)
                for _, row in recent.iterrows():
                    st.write(f"{row['date'].strftime('%Y-%m-%d')} - {row['category']}")
                    st.write(f"{row['description']}: ${row['amount']:.2f}")
                    st.divider()

    elif page == "➕ Add Expense":
        st.header("Add New Expense")
        
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0)
        category = st.selectbox("Category", ["Food", "Transportation", "Housing", "Entertainment", "Other"])
        
        if st.button("Add Expense"):
            expenses = load_expenses()
            expense_id = len(expenses) + 1
            date = datetime.now().strftime('%Y-%m-%d')
            
            new_expense = {
                "id": expense_id,
                "date": date,
                "description": description,
                "amount": amount,
                "category": category
            }
            
            expenses.append(new_expense)
            save_expenses(expenses)
            st.success(f"Expense added successfully (ID: {expense_id})")

    elif page == "📋 View Expenses":
        st.header("View Expenses")
        
        expenses = load_expenses()
        if expenses:
            df = pd.DataFrame(expenses)
            st.dataframe(df)
            
            
            if st.button("Export to CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="expenses_export.csv",
                    mime="text/csv"
                )
        else:
            st.info("No expenses found.")

    elif page == "✏️ Update/Delete":
        st.header("Update or Delete Expense")
        
        expenses = load_expenses()
        if expenses:
            expense_ids = [exp['id'] for exp in expenses]
            selected_id = st.selectbox("Select Expense ID", expense_ids)
            
            expense = next((exp for exp in expenses if exp['id'] == selected_id), None)
            if expense:
                new_description = st.text_input("New Description", expense['description'])
                new_amount = st.number_input("New Amount", value=float(expense['amount']))
                new_category = st.selectbox("New Category", 
                                          ["Food", "Transportation", "Housing", "Entertainment", "Other"],
                                          index=["Food", "Transportation", "Housing", "Entertainment", "Other"].index(expense['category']))
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Update"):
                        expense['description'] = new_description
                        expense['amount'] = new_amount
                        expense['category'] = new_category
                        save_expenses(expenses)
                        st.success(f"Expense ID {selected_id} updated successfully")
                
                with col2:
                    if st.button("Delete"):
                        expenses = [exp for exp in expenses if exp['id'] != selected_id]
                        save_expenses(expenses)
                        st.success(f"Expense ID {selected_id} deleted successfully")
        else:
            st.info("No expenses found.")

    elif page == "💰 Budget Management":
        st.header("Budget Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Set Monthly Budget")
            month = st.selectbox("Select Month", range(1, 13))
            budget_amount = st.number_input("Budget Amount", min_value=0.0)
            
            if st.button("Set Budget"):
                budgets = load_budgets()
                budgets[str(month)] = budget_amount
                save_budgets(budgets)
                st.success(f"Budget for month {month} set to ${budget_amount}")
        
        with col2:
            st.subheader("Check Budget Status")
            check_month = st.selectbox("Select Month to Check", range(1, 13))
            
            if st.button("Check Budget"):
                expenses = load_expenses()
                budgets = load_budgets()
                
                if expenses:
                    df = pd.DataFrame(expenses)
                    df['date'] = pd.to_datetime(df['date'])
                    total = df[df['date'].dt.month == check_month]['amount'].sum()
                    
                    if str(check_month) in budgets:
                        budget = budgets[str(check_month)]
                        st.write(f"Total expenses: ${total:.2f}")
                        st.write(f"Budget: ${budget:.2f}")
                        
                        if total > budget:
                            st.warning(f"You have exceeded the budget by ${total - budget:.2f}!")
                        else:
                            st.success(f"You are within budget! (${budget - total:.2f} remaining)")
                    else:
                        st.info(f"No budget set for month {check_month}")
                else:
                    st.info("No expenses found.")

    elif page == "📈 Analytics":
        st.header("Expense Analytics")
        
        expenses = load_expenses()
        if expenses:
            df = pd.DataFrame(expenses)
            df['date'] = pd.to_datetime(df['date'])
            
            
            st.subheader("Monthly Spending Trend")
            monthly_expenses = df.groupby(df['date'].dt.strftime('%Y-%m'))['amount'].sum().reset_index()
          
            fig = px.line(monthly_expenses, x='date', y='amount')
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            
            st.subheader("Category Breakdown")
            category_expenses = df.groupby('category')['amount'].sum()
          
            fig = px.pie(values=category_expenses.values, names=category_expenses.index)
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Expenses", f"${df['amount'].sum():,.2f}")
            with col2:
                st.metric("Average Expense", f"${df['amount'].mean():,.2f}")
            with col3:
                st.metric("Highest Expense", f"${df['amount'].max():,.2f}")
        else:
            st.info("No expenses found for analysis.")

    elif page == "📄 Reports":
        st.header("Generate Financial Report")

        expenses = load_expenses()
        if expenses:
            df = pd.DataFrame(expenses)
            file_path = export_to_pdf(df)
            with open(file_path, "rb") as pdf_file:
                st.download_button(label="Download Report as PDF", data=pdf_file, file_name="Expense_Report.pdf")
        else:
            st.info("No expenses found to generate a report.")

if __name__ == "__main__":
    main()