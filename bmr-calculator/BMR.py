import json
import math
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


class BMRCalculator:
    """Professional bilingual BMR and daily calorie calculator."""

    SETTINGS_FILE = Path(__file__).with_name("settings.json")

    TEXT = {
        "en": {
            "title": "BMR Calculator",
            "subtitle": "Basal Metabolic Rate & Daily Calorie Calculator",
            "personal_info": "Personal Information",
            "gender": "Gender",
            "male": "Male",
            "female": "Female",
            "age": "Age",
            "years": "years",
            "height": "Height",
            "cm": "cm",
            "weight": "Weight",
            "kg": "kg",
            "activity": "Activity Level",
            "activity_sedentary": "Sedentary — little or no exercise",
            "activity_light": "Lightly active — 1–3 days/week",
            "activity_moderate": "Moderately active — 3–5 days/week",
            "activity_high": "Very active — 6–7 days/week",
            "activity_very_high": "Extra active — hard exercise / physical job",
            "calculate": "Calculate BMR",
            "reset": "Reset",
            "language": "فارسی",
            "result": "Your Results",
            "bmr": "BMR",
            "daily": "Estimated Daily Calories",
            "formula": "Formula",
            "formula_value": "Mifflin–St Jeor",
            "explanation": "BMR is the approximate energy your body needs at complete rest.",
            "daily_explanation": "Daily calories are estimated from your BMR and activity level.",
            "invalid": "Please enter valid values in all fields.",
            "age_error": "Age must be between 13 and 120 years.",
            "height_error": "Height must be between 100 and 250 cm.",
            "weight_error": "Weight must be between 20 and 300 kg.",
            "success": "Calculation completed successfully.",
        },
        "fa": {
            "title": "محاسبه‌گر BMR",
            "subtitle": "محاسبه نرخ متابولیسم پایه و کالری روزانه",
            "personal_info": "اطلاعات شخصی",
            "gender": "جنسیت",
            "male": "مرد",
            "female": "زن",
            "age": "سن",
            "years": "سال",
            "height": "قد",
            "cm": "سانتی‌متر",
            "weight": "وزن",
            "kg": "کیلوگرم",
            "activity": "سطح فعالیت",
            "activity_sedentary": "کم‌تحرک — بدون ورزش یا ورزش بسیار کم",
            "activity_light": "فعالیت سبک — ۱ تا ۳ روز در هفته",
            "activity_moderate": "فعالیت متوسط — ۳ تا ۵ روز در هفته",
            "activity_high": "فعالیت زیاد — ۶ تا ۷ روز در هفته",
            "activity_very_high": "فعالیت خیلی زیاد — ورزش سنگین / کار فیزیکی",
            "calculate": "محاسبه BMR",
            "reset": "بازنشانی",
            "language": "English",
            "result": "نتیجه محاسبه",
            "bmr": "BMR",
            "daily": "کالری تقریبی روزانه",
            "formula": "فرمول",
            "formula_value": "Mifflin–St Jeor",
            "explanation": "BMR انرژی تقریبی موردنیاز بدن در حالت استراحت کامل است.",
            "daily_explanation": "کالری روزانه با توجه به BMR و سطح فعالیت تخمین زده می‌شود.",
            "invalid": "لطفاً تمام فیلدها را با مقادیر معتبر پر کنید.",
            "age_error": "سن باید بین ۱۳ تا ۱۲۰ سال باشد.",
            "height_error": "قد باید بین ۱۰۰ تا ۲۵۰ سانتی‌متر باشد.",
            "weight_error": "وزن باید بین ۲۰ تا ۳۰۰ کیلوگرم باشد.",
            "success": "محاسبه با موفقیت انجام شد.",
        },
    }

    ACTIVITY_FACTORS = {
        "sedentary": 1.20,
        "light": 1.375,
        "moderate": 1.55,
        "high": 1.725,
        "very_high": 1.90,
    }

    def __init__(self, root):
        self.root = root
        self.language = self.load_language()
        self.gender = tk.StringVar(value="male")
        self.age = tk.StringVar()
        self.height = tk.StringVar()
        self.weight = tk.StringVar()
        self.activity = tk.StringVar(value="sedentary")

        self.setup_window()
        self.setup_style()
        self.build_ui()
        self.apply_language()

        self.root.bind("<Return>", lambda _event: self.calculate())
        self.root.bind("<Escape>", lambda _event: self.reset())

    def load_language(self):
        try:
            data = json.loads(self.SETTINGS_FILE.read_text(encoding="utf-8"))
            return data.get("language", "en") if data.get("language") in self.TEXT else "en"
        except (OSError, json.JSONDecodeError):
            return "en"

    def save_language(self):
        try:
            self.SETTINGS_FILE.write_text(
                json.dumps({"language": self.language}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError:
            pass

    def setup_window(self):
        self.root.title("BMR Calculator")
        self.root.geometry("760x680")
        self.root.minsize(650, 600)
        self.root.configure(bg="#10131a")

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TCombobox",
            fieldbackground="#1b202b",
            background="#1b202b",
            foreground="#f5f7fb",
            arrowcolor="#8ab4ff",
            bordercolor="#303746",
            lightcolor="#303746",
            darkcolor="#303746",
            padding=8,
        )

    def build_ui(self):
        self.main = tk.Frame(self.root, bg="#10131a")
        self.main.pack(fill="both", expand=True, padx=30, pady=25)

        self.header = tk.Frame(self.main, bg="#10131a")
        self.header.pack(fill="x")

        self.title_label = tk.Label(
            self.header, bg="#10131a", fg="#f5f7fb",
            font=("Segoe UI", 26, "bold")
        )
        self.title_label.pack()

        self.subtitle_label = tk.Label(
            self.header, bg="#10131a", fg="#929aaa",
            font=("Segoe UI", 11)
        )
        self.subtitle_label.pack(pady=(4, 18))

        self.card = tk.Frame(
            self.main, bg="#171b24",
            highlightbackground="#292f3c", highlightthickness=1
        )
        self.card.pack(fill="x")

        self.form_title = tk.Label(
            self.card, bg="#171b24", fg="#f5f7fb",
            font=("Segoe UI", 14, "bold")
        )
        self.form_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=25, pady=(22, 18))

        self.labels = {}
        fields = [
            ("gender", 1),
            ("age", 2),
            ("height", 3),
            ("weight", 4),
            ("activity", 5),
        ]

        for key, row in fields:
            label = tk.Label(
                self.card, bg="#171b24", fg="#c9ced8",
                font=("Segoe UI", 10, "bold")
            )
            label.grid(row=row, column=0, sticky="w", padx=(25, 15), pady=8)
            self.labels[key] = label

        self.gender_frame = tk.Frame(self.card, bg="#171b24")
        self.gender_frame.grid(row=1, column=1, columnspan=2, sticky="w", padx=10, pady=8)

        self.male_radio = tk.Radiobutton(
            self.gender_frame, variable=self.gender, value="male",
            bg="#171b24", fg="#f5f7fb", selectcolor="#252b38",
            activebackground="#171b24", activeforeground="#f5f7fb",
            font=("Segoe UI", 10)
        )
        self.male_radio.pack(side="left", padx=(0, 22))

        self.female_radio = tk.Radiobutton(
            self.gender_frame, variable=self.gender, value="female",
            bg="#171b24", fg="#f5f7fb", selectcolor="#252b38",
            activebackground="#171b24", activeforeground="#f5f7fb",
            font=("Segoe UI", 10)
        )
        self.female_radio.pack(side="left")

        self.entries = {}
        for key, variable, row in [
            ("age", self.age, 2),
            ("height", self.height, 3),
            ("weight", self.weight, 4),
        ]:
            entry = tk.Entry(
                self.card, textvariable=variable,
                bg="#1b202b", fg="#f5f7fb",
                insertbackground="#f5f7fb",
                relief="flat", bd=0,
                font=("Segoe UI", 11),
            )
            entry.grid(row=row, column=1, sticky="ew", padx=10, pady=8, ipady=8)
            self.entries[key] = entry

        self.units = {}
        for key, row, unit_key in [
            ("age", 2, "years"),
            ("height", 3, "cm"),
            ("weight", 4, "kg"),
        ]:
            label = tk.Label(
                self.card, bg="#171b24", fg="#7f8796",
                font=("Segoe UI", 9)
            )
            label.grid(row=row, column=2, sticky="w", padx=(0, 25))
            self.units[key] = label

        self.activity_combo = ttk.Combobox(
            self.card, textvariable=self.activity,
            state="readonly", font=("Segoe UI", 10), width=34
        )
        self.activity_combo.grid(row=5, column=1, columnspan=2, sticky="ew", padx=(10, 25), pady=8)

        self.card.grid_columnconfigure(1, weight=1)

        self.buttons = tk.Frame(self.main, bg="#10131a")
        self.buttons.pack(fill="x", pady=18)

        self.language_button = tk.Button(
            self.buttons, command=self.toggle_language,
            bg="#252b38", fg="#e7ebf2",
            activebackground="#303746", activeforeground="#ffffff",
            relief="flat", bd=0, cursor="hand2",
            font=("Segoe UI", 10, "bold"), padx=16, pady=11
        )
        self.language_button.pack(side="left")

        self.reset_button = tk.Button(
            self.buttons, command=self.reset,
            bg="#252b38", fg="#e7ebf2",
            activebackground="#303746", activeforeground="#ffffff",
            relief="flat", bd=0, cursor="hand2",
            font=("Segoe UI", 10, "bold"), padx=18, pady=11
        )
        self.reset_button.pack(side="right", padx=(10, 0))

        self.calculate_button = tk.Button(
            self.buttons, command=self.calculate,
            bg="#4f7cff", fg="#ffffff",
            activebackground="#416be0", activeforeground="#ffffff",
            relief="flat", bd=0, cursor="hand2",
            font=("Segoe UI", 10, "bold"), padx=24, pady=11
        )
        self.calculate_button.pack(side="right")

        self.result_card = tk.Frame(
            self.main, bg="#171b24",
            highlightbackground="#292f3c", highlightthickness=1
        )
        self.result_card.pack(fill="x")

        self.result_title = tk.Label(
            self.result_card, bg="#171b24", fg="#f5f7fb",
            font=("Segoe UI", 14, "bold")
        )
        self.result_title.pack(anchor="w", padx=25, pady=(20, 12))

        self.result_values = tk.Frame(self.result_card, bg="#171b24")
        self.result_values.pack(fill="x", padx=25)

        self.bmr_box = self.create_result_box(self.result_values, 0)
        self.daily_box = self.create_result_box(self.result_values, 1)

        self.bmr_name, self.bmr_value = self.bmr_box
        self.daily_name, self.daily_value = self.daily_box

        self.formula_label = tk.Label(
            self.result_card, bg="#171b24", fg="#7f8796",
            font=("Segoe UI", 9)
        )
        self.formula_label.pack(anchor="w", padx=25, pady=(16, 0))

        self.info_label = tk.Label(
            self.result_card, bg="#171b24", fg="#929aaa",
            font=("Segoe UI", 9), justify="left", wraplength=680
        )
        self.info_label.pack(anchor="w", padx=25, pady=(6, 20))

        self.status_label = tk.Label(
            self.main, bg="#10131a", fg="#697386",
            font=("Segoe UI", 9)
        )
        self.status_label.pack(pady=(12, 0))

    def create_result_box(self, parent, column):
        box = tk.Frame(parent, bg="#1d2330")
        box.grid(row=0, column=column, sticky="ew", padx=(0, 10 if column == 0 else 0), pady=4)
        parent.grid_columnconfigure(column, weight=1)

        name = tk.Label(box, bg="#1d2330", fg="#929aaa", font=("Segoe UI", 9, "bold"))
        name.pack(anchor="w", padx=16, pady=(13, 2))

        value = tk.Label(box, bg="#1d2330", fg="#ffffff", font=("Segoe UI", 20, "bold"))
        value.pack(anchor="w", padx=16, pady=(0, 13))

        return name, value

    def apply_language(self):
        t = self.TEXT[self.language]
        rtl = self.language == "fa"

        self.root.title(t["title"])
        self.title_label.config(text=t["title"])
        self.subtitle_label.config(text=t["subtitle"])
        self.form_title.config(text=t["personal_info"])
        self.result_title.config(text=t["result"])

        for key, label in self.labels.items():
            label.config(text=t[key])

        self.male_radio.config(text=t["male"])
        self.female_radio.config(text=t["female"])

        self.units["age"].config(text=t["years"])
        self.units["height"].config(text=t["cm"])
        self.units["weight"].config(text=t["kg"])

        activity_values = [
            ("sedentary", t["activity_sedentary"]),
            ("light", t["activity_light"]),
            ("moderate", t["activity_moderate"]),
            ("high", t["activity_high"]),
            ("very_high", t["activity_very_high"]),
        ]
        self.activity_combo["values"] = [value for _, value in activity_values]
        current_key = self.activity.get()
        keys = [key for key, _ in activity_values]
        if current_key not in keys:
            current_key = "sedentary"
        self.activity.set(dict(activity_values)[current_key])

        self.activity_combo.bind(
            "<<ComboboxSelected>>",
            lambda _event: self.set_activity_key(activity_values)
        )

        self.calculate_button.config(text=t["calculate"])
        self.reset_button.config(text=t["reset"])
        self.language_button.config(text=t["language"])
        self.bmr_name.config(text=t["bmr"])
        self.daily_name.config(text=t["daily"])
        self.formula_label.config(text=f'{t["formula"]}: {t["formula_value"]}')
        self.info_label.config(
            text=f'{t["explanation"]}\n{t["daily_explanation"]}'
        )

        anchor = "e" if rtl else "w"
        justify = "right" if rtl else "left"

        self.title_label.config(anchor=anchor)
        self.subtitle_label.config(anchor=anchor)
        self.form_title.config(anchor=anchor)
        self.result_title.config(anchor=anchor)
        self.formula_label.config(anchor=anchor)
        self.info_label.config(anchor=anchor, justify=justify)

        for entry in self.entries.values():
            entry.config(justify="right" if rtl else "left")

        self.status_label.config(text="")
        self.save_language()

    def set_activity_key(self, activity_values):
        selected = self.activity.get()
        mapping = {value: key for key, value in activity_values}
        self.activity.set(mapping.get(selected, "sedentary"))

    def get_activity_key(self):
        t = self.TEXT[self.language]
        mapping = {
            t["activity_sedentary"]: "sedentary",
            t["activity_light"]: "light",
            t["activity_moderate"]: "moderate",
            t["activity_high"]: "high",
            t["activity_very_high"]: "very_high",
        }
        return mapping.get(self.activity.get(), "sedentary")

    def calculate(self):
        t = self.TEXT[self.language]

        try:
            age = int(self.age.get())
            height = float(self.height.get())
            weight = float(self.weight.get())
        except ValueError:
            messagebox.showerror(t["title"], t["invalid"])
            return

        if not 13 <= age <= 120:
            messagebox.showerror(t["title"], t["age_error"])
            return
        if not 100 <= height <= 250:
            messagebox.showerror(t["title"], t["height_error"])
            return
        if not 20 <= weight <= 300:
            messagebox.showerror(t["title"], t["weight_error"])
            return

        if self.gender.get() == "male":
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

        daily = bmr * self.ACTIVITY_FACTORS[self.get_activity_key()]

        self.bmr_value.config(text=f"{round(bmr):,} kcal/day")
        self.daily_value.config(text=f"{round(daily):,} kcal/day")
        self.status_label.config(text=t["success"])

    def reset(self):
        self.age.set("")
        self.height.set("")
        self.weight.set("")
        self.gender.set("male")
        self.activity.set("sedentary")
        self.bmr_value.config(text="—")
        self.daily_value.config(text="—")
        self.status_label.config(text="")

        self.apply_language()

    def toggle_language(self):
        self.language = "fa" if self.language == "en" else "en"
        self.apply_language()


def main():
    root = tk.Tk()
    BMRCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
