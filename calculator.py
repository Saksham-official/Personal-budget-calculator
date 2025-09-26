import streamlit as st
import datetime

# --- (Core logic functions from your original script - no changes needed) ---

def generate_financial_advice(income, expenses, savings):
    """
    Generates personalized financial advice based on spending patterns.
    """
    advice_list = []
    
    if income == 0:
        return "Your income is zero. Please enter a valid income to get advice."
        
    # Added a check to prevent division by zero if income is positive but small
    try:
        savings_percentage = (savings / income) * 100
    except ZeroDivisionError:
        savings_percentage = 0

    if savings > 0:
        advice_list.append(
            f"Great job! You saved ${savings:,.2f} this month. "
            f"That's {savings_percentage:.2f}% of your income. 🎉"
        )
        if savings_percentage >= 20:
            advice_list.append(
                "Saving over 20% is fantastic! You're on a great path for financial security."
            )
        else:
            advice_list.append(
                "Try to aim for a 20% savings rate for a healthier financial future."
            )
    else:
        advice_list.append(
            f"You have a deficit of ${abs(savings):,.2f}. "
            "It's crucial to review your spending and create a budget."
        )

    non_zero_expenses = {k: v for k, v in expenses.items() if v > 0}
    
    if non_zero_expenses:
        largest_expense_category = max(non_zero_expenses, key=lambda k: non_zero_expenses[k])
        largest_expense_value = non_zero_expenses[largest_expense_category]
        try:
            expense_percentage = (largest_expense_value / income) * 100
        except ZeroDivisionError:
            expense_percentage = 0
            
        advice_list.append(
            f"Your largest spending category is '{largest_expense_category}' at ${largest_expense_value:,.2f}, "
            f"which is {expense_percentage:.2f}% of your income."
        )

    return "\n".join(advice_list)

# --- (Streamlit App Interface) ---

st.set_page_config(page_title="Personal Budget Calculator", layout="centered")

st.title("💰 Monthly Expense & Savings Tracker")

# Use a form to group inputs
with st.form("budget_form"):
    st.header("Your Income")
    # Use st.number_input for user input instead of input()
    monthly_income = st.number_input("Enter your total monthly income:", min_value=0.0, format="%.2f")

    st.header("Your Expenses")
    categories = [
        'Rent/Mortgage', 'Groceries', 'Utilities', 
        'Transportation', 'Entertainment', 'Other'
    ]
    expenses = {}
    # Create number inputs for each category
    for category in categories:
        expenses[category] = st.number_input(f"Enter amount for {category}:", min_value=0.0, format="%.2f")

    # The button to trigger the calculations
    submitted = st.form_submit_button("Generate Report")

# This block runs only when the button is clicked
if submitted:
    total_expenses = sum(expenses.values())
    savings = monthly_income - total_expenses
    advice = generate_financial_advice(monthly_income, expenses, savings)
    
    # --- Generate the report string (same as before) ---
    report = f"""
========================================
   Monthly Financial Report
========================================

Income: ${monthly_income:,.2f}

--- Expenses Breakdown ---
"""
    for category, amount in expenses.items():
        report += f"- {category:<20}: ${amount:,.2f}\n"

    report += f"""
----------------------------------------
Total Expenses: ${total_expenses:,.2f}
----------------------------------------

**Final Savings:** ${savings:,.2f}

========================================
   Personalized Advice
========================================
{advice}
========================================
"""
    
    st.subheader("Your Financial Report")
    # Use st.code to display the report in a formatted block
    st.code(report, language=None)
    
    st.success("Report generated successfully!")
    
    # --- Add a download button ---
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    st.download_button(
        label="📥 Download Report as .txt",
        data=report,
        file_name=f"financial_report_{timestamp}.txt",
        mime="text/plain"
    )