import json
import tkinter as tk
from tkinter import messagebox
from pathlib import Path


class BMICalculator:
    # -----------------------------
    # Colors
    # -----------------------------
    BG = "#0f172a"
    CARD = "#1e293b"
    INPUT = "#334155"
    TEXT = "#f8fafc"
    MUTED = "#94a3b8"
    ACCENT = "#38bdf8"
    SUCCESS = "#22c55e"
    WARNING = "#f59e0b"
    DANGER = "#ef4444"

    def __init__(self, root):
        self.root = root

        # File used to remember the selected language
        self.language_file = Path(__file__).with_name("settings.json")

        self.language = self.load_language()

        # -----------------------------
        # Translations
        # -----------------------------
        self.translations = {
            "en": {
                "title": "BMI Calculator",
                "subtitle": "Calculate your Body Mass Index",

                "height": "Height",
                "weight": "Weight",

                "cm": "cm",
                "kg": "kg",

                "calculate": "Calculate BMI",
                "reset": "Reset",

                "your_bmi": "Your BMI: —",
                "initial": "Enter your height and weight to calculate.",

                "healthy_range": "Healthy BMI range: 18.5 – 24.9",

                "status": "Status: {}",

                "healthy_weight":
                    "Estimated healthy weight range: {:.1f} – {:.1f} kg",

                # Errors
                "invalid": "Please enter valid numbers.",
                "positive":
                    "Height and weight must be greater than zero.",

                "height_error":
                    "Height must be between 50 and 250 cm.",

                "weight_error":
                    "Weight must be between 10 and 500 kg.",

                "invalid_title": "Invalid Input",
                "height_title": "Invalid Height",
                "weight_title": "Invalid Weight",

                # Categories
                "underweight": "Underweight",
                "normal": "Normal weight",
                "overweight": "Overweight",
                "obesity": "Obesity",

                "footer":
                    "Python • Tkinter • BMI Calculator",
            },

            "fa": {
                "title": "محاسبه‌گر شاخص توده بدنی",
                "subtitle": "شاخص توده بدنی خود را محاسبه کنید",

                "height": "قد",
                "weight": "وزن",

                "cm": "سانتی‌متر",
                "kg": "کیلوگرم",

                "calculate": "محاسبه BMI",
                "reset": "بازنشانی",

                "your_bmi": "BMI شما: —",
                "initial": "قد و وزن خود را وارد کنید.",

                "healthy_range":
                    "محدوده BMI سالم: ۱۸٫۵ تا ۲۴٫۹",

                "status": "وضعیت: {}",

                "healthy_weight":
                    "محدوده وزن سالم: {:.1f} تا {:.1f} کیلوگرم",

                # Errors
                "invalid":
                    "لطفاً اعداد معتبر وارد کنید.",

                "positive":
                    "قد و وزن باید بیشتر از صفر باشند.",

                "height_error":
                    "قد باید بین ۵۰ تا ۲۵۰ سانتی‌متر باشد.",

                "weight_error":
                    "وزن باید بین ۱۰ تا ۵۰۰ کیلوگرم باشد.",

                "invalid_title":
                    "ورودی نامعتبر",

                "height_title":
                    "قد نامعتبر",

                "weight_title":
                    "وزن نامعتبر",

                # Categories
                "underweight": "کمبود وزن",
                "normal": "وزن متعادل",
                "overweight": "اضافه وزن",
                "obesity": "چاقی",

                "footer":
                    "Python • Tkinter • محاسبه‌گر BMI",
            },
        }

        # -----------------------------
        # Variables
        # -----------------------------
        self.height_var = tk.StringVar()
        self.weight_var = tk.StringVar()

        self.build_ui()
        self.apply_language()

    # =========================================================
    # Language
    # =========================================================

    def load_language(self):
        """Load the saved language from settings.json."""

        try:
            data = json.loads(
                self.language_file.read_text(encoding="utf-8")
            )

            language = data.get("language", "en")

            if language in ("en", "fa"):
                return language

        except (FileNotFoundError, json.JSONDecodeError):
            pass

        return "en"

    def save_language(self):
        """Save the selected language."""

        self.language_file.write_text(
            json.dumps(
                {"language": self.language},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def t(self, key):
        """Return translated text."""

        return self.translations[self.language][key]

    def toggle_language(self):
        """Switch between English and Persian."""

        if self.language == "en":
            self.language = "fa"
        else:
            self.language = "en"

        self.save_language()
        self.apply_language()

    # =========================================================
    # User Interface
    # =========================================================

    def build_ui(self):

        self.root.configure(bg=self.BG)

        self.root.geometry("760x650")
        self.root.minsize(650, 580)

        # -----------------------------
        # Top section
        # -----------------------------

        top = tk.Frame(
            self.root,
            bg=self.BG
        )

        top.pack(
            fill="x",
            padx=35,
            pady=(22, 8)
        )

        self.language_button = tk.Button(
            top,
            command=self.toggle_language,
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD,
            fg=self.TEXT,
            activebackground=self.INPUT,
            activeforeground=self.TEXT,
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=7,
        )

        self.language_button.pack(side="right")

        # -----------------------------
        # Title
        # -----------------------------

        self.title_label = tk.Label(
            self.root,
            font=("Segoe UI", 27, "bold"),
            bg=self.BG,
            fg=self.TEXT,
        )

        self.title_label.pack(
            pady=(4, 3)
        )

        self.subtitle_label = tk.Label(
            self.root,
            font=("Segoe UI", 11),
            bg=self.BG,
            fg=self.MUTED,
        )

        self.subtitle_label.pack()

        # -----------------------------
        # Main Card
        # -----------------------------

        self.card = tk.Frame(
            self.root,
            bg=self.CARD,
            padx=30,
            pady=25,
        )

        self.card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=18,
        )

        # -----------------------------
        # Height
        # -----------------------------

        self.height_label = tk.Label(
            self.card,
            font=("Segoe UI", 12, "bold"),
            bg=self.CARD,
            fg=self.TEXT,
        )

        self.height_label.grid(
            row=0,
            column=0,
            sticky="w",
            pady=10,
        )

        self.height_entry = tk.Entry(
            self.card,
            textvariable=self.height_var,
            font=("Segoe UI", 12),
            bg=self.INPUT,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            width=25,
        )

        self.height_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=18,
            pady=10,
            ipady=9,
        )

        self.height_unit = tk.Label(
            self.card,
            font=("Segoe UI", 11),
            bg=self.CARD,
            fg=self.MUTED,
        )

        self.height_unit.grid(
            row=0,
            column=2,
            sticky="e",
        )

        # -----------------------------
        # Weight
        # -----------------------------

        self.weight_label = tk.Label(
            self.card,
            font=("Segoe UI", 12, "bold"),
            bg=self.CARD,
            fg=self.TEXT,
        )

        self.weight_label.grid(
            row=1,
            column=0,
            sticky="w",
            pady=10,
        )

        self.weight_entry = tk.Entry(
            self.card,
            textvariable=self.weight_var,
            font=("Segoe UI", 12),
            bg=self.INPUT,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            width=25,
        )

        self.weight_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=18,
            pady=10,
            ipady=9,
        )

        self.weight_unit = tk.Label(
            self.card,
            font=("Segoe UI", 11),
            bg=self.CARD,
            fg=self.MUTED,
        )

        self.weight_unit.grid(
            row=1,
            column=2,
            sticky="e",
        )

        # -----------------------------
        # Buttons
        # -----------------------------

        buttons = tk.Frame(
            self.card,
            bg=self.CARD
        )

        buttons.grid(
            row=2,
            column=0,
            columnspan=3,
            pady=24,
        )

        self.calculate_button = tk.Button(
            buttons,
            command=self.calculate_bmi,
            font=("Segoe UI", 12, "bold"),
            bg=self.ACCENT,
            fg="#0f172a",
            activebackground="#7dd3fc",
            relief="flat",
            cursor="hand2",
            padx=24,
            pady=10,
        )

        self.calculate_button.pack(
            side="left",
            padx=6,
        )

        self.reset_button = tk.Button(
            buttons,
            command=self.reset,
            font=("Segoe UI", 12),
            bg=self.INPUT,
            fg=self.TEXT,
            activebackground="#475569",
            activeforeground=self.TEXT,
            relief="flat",
            cursor="hand2",
            padx=24,
            pady=10,
        )

        self.reset_button.pack(
            side="left",
            padx=6,
        )

        # -----------------------------
        # Result
        # -----------------------------

        self.result_frame = tk.Frame(
            self.card,
            bg=self.INPUT,
            padx=20,
            pady=18,
        )

        self.result_frame.grid(
            row=3,
            column=0,
            columnspan=3,
            sticky="ew",
        )

        self.bmi_label = tk.Label(
            self.result_frame,
            font=("Segoe UI", 22, "bold"),
            bg=self.INPUT,
            fg=self.TEXT,
        )

        self.bmi_label.pack()

        self.status_label = tk.Label(
            self.result_frame,
            font=("Segoe UI", 12),
            bg=self.INPUT,
            fg=self.MUTED,
        )

        self.status_label.pack(
            pady=(7, 0)
        )

        self.range_label = tk.Label(
            self.result_frame,
            font=("Segoe UI", 10),
            bg=self.INPUT,
            fg=self.MUTED,
        )

        self.range_label.pack(
            pady=(8, 0)
        )

        # -----------------------------
        # Footer
        # -----------------------------

        self.footer_label = tk.Label(
            self.root,
            font=("Segoe UI", 9),
            bg=self.BG,
            fg=self.MUTED,
        )

        self.footer_label.pack(
            pady=(0, 13)
        )

        self.card.columnconfigure(
            1,
            weight=1
        )

        # Keyboard shortcuts
        self.root.bind(
            "<Return>",
            lambda event: self.calculate_bmi()
        )

        self.root.bind(
            "<Escape>",
            lambda event: self.reset()
        )

    # =========================================================
    # Apply Language
    # =========================================================

    def apply_language(self):

        rtl = self.language == "fa"

        self.root.title(
            self.t("title")
        )

        self.title_label.config(
            text=self.t("title")
        )

        self.subtitle_label.config(
            text=self.t("subtitle")
        )

        self.height_label.config(
            text=self.t("height")
        )

        self.weight_label.config(
            text=self.t("weight")
        )

        self.height_unit.config(
            text=self.t("cm")
        )

        self.weight_unit.config(
            text=self.t("kg")
        )

        self.calculate_button.config(
            text=self.t("calculate")
        )

        self.reset_button.config(
            text=self.t("reset")
        )

        self.footer_label.config(
            text=self.t("footer")
        )

        # Language button shows the language
        # that the user can switch to.
        if rtl:
            self.language_button.config(
                text="English"
            )
        else:
            self.language_button.config(
                text="فارسی"
            )

        # Input alignment
        justify = "right" if rtl else "left"

        self.height_entry.config(
            justify=justify
        )

        self.weight_entry.config(
            justify=justify
        )

        # Mirror the main layout for Persian
        if rtl:

            self.height_label.grid_configure(
                column=2,
                sticky="e"
            )

            self.height_entry.grid_configure(
                column=1
            )

            self.height_unit.grid_configure(
                column=0,
                sticky="w"
            )

            self.weight_label.grid_configure(
                column=2,
                sticky="e"
            )

            self.weight_entry.grid_configure(
                column=1
            )

            self.weight_unit.grid_configure(
                column=0,
                sticky="w"
            )

        else:

            self.height_label.grid_configure(
                column=0,
                sticky="w"
            )

            self.height_entry.grid_configure(
                column=1
            )

            self.height_unit.grid_configure(
                column=2,
                sticky="e"
            )

            self.weight_label.grid_configure(
                column=0,
                sticky="w"
            )

            self.weight_entry.grid_configure(
                column=1
            )

            self.weight_unit.grid_configure(
                column=2,
                sticky="e"
            )

        # Reset displayed result text
        self.bmi_label.config(
            text=self.t("your_bmi")
        )

        self.status_label.config(
            text=self.t("initial")
        )

        self.range_label.config(
            text=self.t("healthy_range")
        )

    # =========================================================
    # BMI Calculation
    # =========================================================

    def calculate_bmi(self):

        try:
            height_cm = float(
                self.height_var.get().strip()
            )

            weight_kg = float(
                self.weight_var.get().strip()
            )

        except ValueError:

            messagebox.showerror(
                self.t("invalid_title"),
                self.t("invalid")
            )

            return

        # Positive numbers
        if height_cm <= 0 or weight_kg <= 0:

            messagebox.showerror(
                self.t("invalid_title"),
                self.t("positive")
            )

            return

        # Height validation
        if not 50 <= height_cm <= 250:

            messagebox.showerror(
                self.t("height_title"),
                self.t("height_error")
            )

            return

        # Weight validation
        if not 10 <= weight_kg <= 500:

            messagebox.showerror(
                self.t("weight_title"),
                self.t("weight_error")
            )

            return

        # Convert centimeters to meters
        height_m = height_cm / 100

        # BMI formula
        bmi = weight_kg / (height_m ** 2)

        category, color = self.get_category(
            bmi
        )

        # Healthy weight range
        healthy_min = (
            18.5 * height_m ** 2
        )

        healthy_max = (
            24.9 * height_m ** 2
        )

        # Result
        bmi_text = self.t(
            "your_bmi"
        ).replace(
            "—",
            f"{bmi:.1f}"
        )

        self.bmi_label.config(
            text=bmi_text,
            fg=color
        )

        self.status_label.config(
            text=self.t(
                "status"
            ).format(category),
            fg=color
        )

        self.range_label.config(
            text=self.t(
                "healthy_weight"
            ).format(
                healthy_min,
                healthy_max
            )
        )

    # =========================================================
    # BMI Category
    # =========================================================

    def get_category(self, bmi):

        if bmi < 18.5:
            return (
                self.t("underweight"),
                self.ACCENT
            )

        if bmi < 25:
            return (
                self.t("normal"),
                self.SUCCESS
            )

        if bmi < 30:
            return (
                self.t("overweight"),
                self.WARNING
            )

        return (
            self.t("obesity"),
            self.DANGER
        )

    # =========================================================
    # Reset
    # =========================================================

    def reset(self):

        self.height_var.set("")
        self.weight_var.set("")

        self.bmi_label.config(
            text=self.t("your_bmi"),
            fg=self.TEXT
        )

        self.status_label.config(
            text=self.t("initial"),
            fg=self.MUTED
        )

        self.range_label.config(
            text=self.t("healthy_range")
        )


def main():
    root = tk.Tk()

    BMICalculator(root)

    root.mainloop()


if __name__ == "__main__":
    main()