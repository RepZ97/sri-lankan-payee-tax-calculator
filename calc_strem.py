import streamlit as st

def calculate_take_home_salary(gross_salary):
    if gross_salary <= 150000:
        etf_deduction = 0.08 * 0.60 * gross_salary
        take_home_salary = gross_salary - etf_deduction
        return take_home_salary, 0, etf_deduction  # No tax if salary is 150000 or below
    
    tax_brackets = [
        (83334, 0.06),  # 6% on next 83334
        (41667, 0.18),  # 18% on next 41667
        (41667, 0.30),  # 30% on next 41667
    ]
    
    remaining_salary = gross_salary - 150000
    tax = 0
    
    for bracket, rate in tax_brackets:
        if remaining_salary > bracket:
            tax += bracket * rate
            remaining_salary -= bracket
        else:
            tax += remaining_salary * rate
            remaining_salary = 0
            break
    
    # Anything beyond the brackets is taxed at 36%
    if remaining_salary > 0:
        tax += remaining_salary * 0.36
    
    etf_deduction = 0.08 * 0.60 * gross_salary  # Deduct 8% from 60% of gross salary
    take_home_salary = gross_salary - tax - etf_deduction
    
    return take_home_salary, tax, etf_deduction

# Streamlit UI
st.title("Take-Home Salary Calculator")

gross_salary = st.number_input("Enter your gross salary:", min_value=0.0, step=1000.0, format="%.2f")

if st.button("Calculate"):
    if gross_salary > 0:
        take_home, total_tax, etf_deduction = calculate_take_home_salary(gross_salary)
        st.write(f"**Your take-home salary is:** {take_home:.2f}")
        st.write(f"**Total Tax Deduction:** {total_tax:.2f}")
        st.write(f"**ETF Deduction:** {etf_deduction:.2f}")
    else:
        st.error("Please enter a valid salary amount.")
