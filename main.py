from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class GovernmentsCutCalc(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=10, **kwargs)

        self.add_widget(Label(text="Enter your gross salary:"))

        self.salary_input = TextInput(multiline=False, input_filter="float")
        self.add_widget(self.salary_input)

        self.calculate_button = Button(text="Calculate")
        self.calculate_button.bind(on_press=self.calculate_take_home)
        self.add_widget(self.calculate_button)

        self.result_label = Label(text="")
        self.add_widget(self.result_label)

    def calculate_take_home(self, instance):
        try:
            gross_salary = float(self.salary_input.text)
            take_home, total_tax, etf_deduction = self.compute_salary(gross_salary)
            self.result_label.text = (
                f"Take-Home Salary: {take_home:.2f}\n"
                f"Total Tax Deduction: {total_tax:.2f}\n"
                f"ETF Deduction: {etf_deduction:.2f}"
            )
        except ValueError:
            self.result_label.text = "Please enter a valid salary."

    def compute_salary(self, gross_salary):
        if gross_salary <= 150000:
            etf_deduction = 0.08 * 0.60 * gross_salary
            return gross_salary - etf_deduction, 0, etf_deduction
        
        tax_brackets = [
            (83334, 0.06),  
            (41667, 0.18),  
            (41667, 0.30),  
        ]

        remaining_salary = gross_salary - 150000
        total_tax = 0

        for bracket, rate in tax_brackets:
            if remaining_salary > bracket:
                total_tax += bracket * rate
                remaining_salary -= bracket
            else:
                total_tax += remaining_salary * rate
                remaining_salary = 0
                break

        if remaining_salary > 0:
            total_tax += remaining_salary * 0.36

        etf_deduction = 0.08 * 0.60 * gross_salary
        take_home_salary = gross_salary - total_tax - etf_deduction
        return take_home_salary, total_tax, etf_deduction

class GovernmentsCutApp(App):
    def build(self):
        return GovernmentsCutCalc()

if __name__ == "__main__":
    GovernmentsCutApp().run()
