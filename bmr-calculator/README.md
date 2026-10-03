# 🔥 BMR Calculator

A modern bilingual desktop **BMR (Basal Metabolic Rate) Calculator** built with **Python and Tkinter**.

This project calculates an estimated BMR using the **Mifflin–St Jeor equation** and also estimates daily calorie needs based on activity level.

## ✨ Features

- 🔥 BMR calculation
- 🍽️ Estimated daily calorie needs
- 🇬🇧 English / 🇮🇷 Persian interface
- 🌐 RTL / LTR support
- 👤 Male / Female selection
- 📊 Activity level selection
- ✅ Input validation
- 💾 Saved language preference
- ⌨️ Enter to calculate
- ⌨️ Escape to reset
- 🌙 Modern dark UI
- 🧱 Object-Oriented Programming
- 🚫 No external packages

## 🧮 BMR Formula

The project uses the **Mifflin–St Jeor** equation.

### Male

```text
BMR = 10 × weight + 6.25 × height − 5 × age + 5
```

### Female

```text
BMR = 10 × weight + 6.25 × height − 5 × age − 161
```

Weight is measured in kilograms and height in centimeters.

## 📊 Activity Levels

| Activity | Multiplier |
|---|---:|
| Sedentary | 1.20 |
| Lightly active | 1.375 |
| Moderately active | 1.55 |
| Very active | 1.725 |
| Extra active | 1.90 |

Estimated daily calories are calculated as:

```text
Daily Calories ≈ BMR × Activity Factor
```

## ▶️ Run

```bash
python BMR.py
```

Windows:

```bash
py BMR.py
```

## 📂 Structure

```text
bmr-calculator/
├── BMR.py
└── README.md
```

`settings.json` is generated automatically when the app saves the selected language.

## ⌨️ Keyboard Shortcuts

| Key | Action |
|---|---|
| Enter | Calculate |
| Escape | Reset |

## 🎯 Learning Goals

This project practices:

- Python fundamentals
- Tkinter GUI development
- Object-Oriented Programming
- Classes and methods
- Input validation
- JSON file handling
- Event handling
- Mathematical formulas
- Bilingual UI design
- RTL / LTR interface handling

## ⚠️ Note

BMR and daily calorie values are estimates, not medical or nutritional diagnoses. Individual energy needs can vary.

## 👨‍💻 Author

**KeramatNia**

Building Python projects step by step.
