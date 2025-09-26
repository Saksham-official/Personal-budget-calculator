import datetime

def get_positive_float_input(prompt):
    """
    Prompts the user for a number and ensures it's a valid, non-negative float.
    Keeps asking until valid input is received.
    """
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a positive number or zero.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

def get_user_expenses():
    """
    Gathers expense details from the user for predefined categories.
    """
    expenses = {}
    categories = [
        'Rent/Mortgage', 
        'Groceries', 
        'Utilities', 
        'Transportation', 
        'Entertainment', 
        'Other'
    ]
    
    print("\nPlease enter your expenses for this month:")
    for category in categories:
        prompt = f"  Enter amount for {category}: $"
        expenses[category] = get_positive_float_input(prompt)
    return expenses

def generate_financial_advice(income, expenses, savings):
    """
    Generates personalized financial advice based on spending patterns.
    """
    advice_list = []
    
    if income == 0:
        return "Your income is zero. Please enter a valid income to get advice."
        
    savings_percentage = (savings / income) * 100

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
        # Use a lambda function for clarity with the type checker
        largest_expense_category = max(non_zero_expenses, key=lambda k: non_zero_expenses[k])
        largest_expense_value = non_zero_expenses[largest_expense_category]
        expense_percentage = (largest_expense_value / income) * 100
        advice_list.append(
            f"Your largest spending category is '{largest_expense_category}' at ${largest_expense_value:,.2f}, "
            f"which is {expense_percentage:.2f}% of your income."
        )

    return "\n".join(advice_list)

def save_report_to_file(report_content):
    """
    Saves the financial report to a text file with a unique timestamp.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"financial_report_{timestamp}.txt"
    
    try:
        with open(filename, 'w') as file:
            file.write(report_content)
        print(f"\n✅ Success! Your report has been saved to '{filename}'")
    except IOError as e:
        print(f"\n❌ Error: Could not save the report. {e}")


if __name__ == "__main__":
    print("--- Monthly Expense and Savings Tracker ---")

    monthly_income = get_positive_float_input("Enter your total monthly income: $")
    expenses = get_user_expenses()

    total_expenses = sum(expenses.values())
    savings = monthly_income - total_expenses

    advice = generate_financial_advice(monthly_income, expenses, savings)
    
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
    
    print(report)

    save_report_to_file(report)