import tkinter as tk
from tkinter import messagebox

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

def calculate_and_display():
    try:
        gross_salary = float(entry.get())
        take_home, total_tax, etf_deduction = calculate_take_home_salary(gross_salary)
        messagebox.showinfo("Take-Home Salary", f"Your take-home salary is: {take_home:.2f}\nTotal Tax Deduction: {total_tax:.2f}\nETF Deduction: {etf_deduction:.2f}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number")

# Create GUI
root = tk.Tk()
root.title("Take-Home Salary Calculator")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(pady=10)

tk.Label(frame, text="Enter your gross salary:").grid(row=0, column=0, padx=5, pady=5)
entry = tk.Entry(frame)
entry.grid(row=0, column=1, padx=5, pady=5)

tk.Button(frame, text="Calculate", command=calculate_and_display).grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
