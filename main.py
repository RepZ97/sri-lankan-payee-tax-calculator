from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout


class GovernmentsCutCalc(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ** Top-Right Section: Tax Version Selector & Button **
        top_right_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(300, 30),
                 pos_hint={'right': 1, 'top': 1}, padding=1, spacing=20,)

        self.version_label = Label(text="Select tax version:", size_hint=(None, None), size=(120, 30))
        top_right_layout.add_widget(self.version_label)

        self.version_spinner = Spinner(text="Upcoming", values=["Upcoming", "Present"],
                           size_hint=(None, None), size=(120, 30))
        top_right_layout.add_widget(self.version_spinner)

        self.add_widget(top_right_layout)

        self.calculate_button = Button(text="Go", size_hint=(None, None), size=(400, 50),
                           pos_hint={'center_x': 0.5, 'top': 0.5})
        self.calculate_button.bind(on_press=self.calculate_take_home)
        self.add_widget(self.calculate_button)

        # ** Main Section: Salary Input & Results **
        self.salary_label = Label(text="Enter your gross salary:", size_hint=(None, None),
                                  size=(200, 40), pos_hint={'center_x': 0.5, 'top': 0.7})
        self.add_widget(self.salary_label)

        self.salary_input = TextInput(multiline=False, input_filter="float", size_hint=(None, None),
                                      size=(400, 50), pos_hint={'center_x': 0.5, 'top': 0.6})
        self.add_widget(self.salary_input)

        self.result_label = Label(text="", size_hint=(None, None), size=(400, 80),
                                  pos_hint={'center_x': 0.5, 'top': 0.4})
        self.add_widget(self.result_label)

    def calculate_take_home(self, instance):
        try:
            gross_salary = float(self.salary_input.text)
            selected_version = self.version_spinner.text
            take_home, total_tax, etf_deduction = self.compute_salary(gross_salary, selected_version)

            self.result_label.text = (
                f"Take-Home Salary: {take_home:.2f}\n"
                f"Total Tax Deduction: {total_tax:.2f}\n"
                f"ETF Deduction: {etf_deduction:.2f}"
            )
        except ValueError:
            self.result_label.text = "Please enter a valid salary."

    def compute_salary(self, gross_salary, version):
        # Define tax brackets for each version
        tax_brackets = {
            "Upcoming": [
                (83334, 0.06),
                (41667, 0.18),
                (41667, 0.30),
            ],
            "Present": [  # Modify these values as needed
                (80000, 0.05),
                (40000, 0.15),
                (40000, 0.28),
            ],
        }

        if gross_salary <= 150000:
            etf_deduction = 0.08 * 0.60 * gross_salary
            return gross_salary - etf_deduction, 0, etf_deduction

        remaining_salary = gross_salary - 150000
        total_tax = 0

        for bracket, rate in tax_brackets[version]:
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
