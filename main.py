from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from utils.data_handler import load_and_plot_histogram
import os

class GovernmentsCutCalc(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # top right hand side layout parent flex box
        parent_layout = BoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            size=(120, 210),
            pos_hint={"right": 1, "top": 1},
            spacing=20,
        )

        top_right_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            size=(300, 30),
            pos_hint={"right": 1, "top": 1},
            padding=1,
            spacing=20,
        )

        self.version_label = Label(
            text="Select tax version:", size_hint=(None, None), size=(120, 30)
        )
        top_right_layout.add_widget(self.version_label)

        # drop down for selecting tax versions
        self.version_spinner = Spinner(
            text="Upcoming",
            values=["Upcoming", "Present"],
            size_hint=(None, None),
            size=(120, 30),
        )
        top_right_layout.add_widget(self.version_spinner)

        # histgram button layout box
        hist_button_layout = BoxLayout(
            size_hint=(None, None),
            size=(120, 30),
            pos_hint={"center_x": 0.17},
            padding=(0, 60, 0, 0),
        )
        self.hist_button = Button(
            text="Global Rates", size_hint=(None, None), size=(120, 30)
        )
        self.hist_button.bind(on_press=self.show_histogram)
        hist_button_layout.add_widget(self.hist_button)

        # EPF layout box
        etf_layout = BoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            size=(300, 80),
            pos_hint={"center_x": 0.5},
        )

        self.etf_label = Label(
            text="Salary Percentage Eligible \nfor EPF Deductions: 60%",
            size_hint=(None, None),
            size=(200, 50),
        )
        etf_layout.add_widget(self.etf_label)

        self.etf_slider = Slider(
            min=0,
            max=1,
            value=0.6,
            step=0.1,
            size_hint=(None, None),
            size=(205, 30),
            pos_hint={"center_x": 0.33},
        )
        self.etf_slider.bind(value=self.update_etf_label)
        etf_layout.add_widget(self.etf_slider)

        parent_layout.add_widget(top_right_layout)
        parent_layout.add_widget(hist_button_layout)
        parent_layout.add_widget(etf_layout)

        self.add_widget(parent_layout)

        # isolated elements
        self.calculate_button = Button(
            text="Go",
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={"center_x": 0.5, "top": 0.5},
        )
        self.calculate_button.bind(on_press=self.calculate_take_home)
        self.add_widget(self.calculate_button)

        self.salary_label = Label(
            text="Enter your gross salary:",
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={"center_x": 0.5, "top": 0.7},
        )
        self.add_widget(self.salary_label)

        self.salary_input = TextInput(
            multiline=False,
            input_filter="float",
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={"center_x": 0.5, "top": 0.6},
        )
        self.add_widget(self.salary_input)

        self.result_label = Label(
            text="",
            size_hint=(None, None),
            size=(400, 80),
            pos_hint={"center_x": 0.5, "top": 0.4},
        )
        self.add_widget(self.result_label)

    def update_etf_label(self, instance, value):
        self.etf_label.text = (
            f"Salary Percentage Eligible \nfor EPF Deductions: {int(value * 100)}%"
        )

    def calculate_take_home(self, instance):
        try:
            gross_salary = float(self.salary_input.text)
            selected_version = self.version_spinner.text
            etf_percentage = self.etf_slider.value
            take_home, total_tax, etf_deduction = self.compute_salary(
                gross_salary, selected_version, etf_percentage
            )

            # result display format
            self.result_label.text = (
                f"Take-Home Salary: LKR {take_home:.2f}\n"
                f"Total Tax Deduction: LKR {total_tax:.2f}\n"
                f"EPF Deduction: LKR {etf_deduction:.2f}"
            )
        except ValueError:
            self.result_label.text = "Please enter a valid salary."

    def compute_salary(self, gross_salary, version, etf_percentage):
        tax_brackets = {
            "Upcoming": [
                (83334, 0.06),
                (41667, 0.18),
                (41667, 0.24),
                (41667, 0.30),
            ],
            "Present": [
                (41667, 0.06),
                (41666, 0.12),
                (41667, 0.18),
                (41667, 0.24),
                (41667, 0.30),
            ],
        }

        if version == "Upcoming" and gross_salary <= 150000:
            etf_deduction = 0.08 * etf_percentage * gross_salary
            return gross_salary - etf_deduction, 0, etf_deduction
        elif version == "Present" and gross_salary <= 100000:
            etf_deduction = 0.08 * etf_percentage * gross_salary
            return gross_salary - etf_deduction, 0, etf_deduction

        # lowest taxable limit declaration based on the version
        lower_limit = 100000 if version == "Present" else 150000

        # taxable income
        remaining_salary = gross_salary - lower_limit
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

        etf_deduction = 0.08 * etf_percentage * gross_salary
        take_home_salary = gross_salary - total_tax - etf_deduction
        return take_home_salary, total_tax, etf_deduction

    def show_histogram(self, instance):
        plot_path = load_and_plot_histogram()

        if not plot_path:
            self.result_label.text = "Error loading histogram!"
            return

        hist_popup = Popup(title="Global Tax Rates", size_hint=(0.8, 0.8))
        hist_image = Image(source=plot_path)
        hist_popup.add_widget(hist_image)

        def on_dismiss(*args):
            if os.path.exists(plot_path):
                os.remove(plot_path)

        hist_popup.bind(on_dismiss=on_dismiss)
        hist_popup.open()


class GovernmentsCutApp(App):
    def build(self):
        return GovernmentsCutCalc()


if __name__ == "__main__":
    GovernmentsCutApp().run()
