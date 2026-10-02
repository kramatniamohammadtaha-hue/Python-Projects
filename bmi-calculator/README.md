# 🧮 BMI Calculator

A professional bilingual desktop **BMI Calculator** built with **Python** and **Tkinter**.

This project is a polished version of my original BMI Calculator, redesigned with a modern graphical interface, bilingual support, input validation, saved language preferences, and a cleaner Object-Oriented structure.

## ✨ Features

- 🇬🇧 English language support
- 🇮🇷 Persian language support
- ↔️ RTL / LTR layout switching
- 💾 Saves the selected language
- 🧮 BMI calculation
- 📊 BMI category detection
- ⚖️ Estimated healthy weight range
- ⚠️ Input validation
- ❌ Bilingual error messages
- 🔄 Reset functionality
- ⌨️ Enter key to calculate
- ⎋ Escape key to reset
- 🎨 Modern dark user interface
- 📱 Resizable application window
- 🧱 Object-Oriented Python structure
- 📦 No external libraries required

## 📊 BMI Categories

| BMI | English | فارسی |
|---:|---|---|
| Below 18.5 | Underweight | کمبود وزن |
| 18.5 – 24.9 | Normal weight | وزن متعادل |
| 25 – 29.9 | Overweight | اضافه وزن |
| 30+ | Obesity | چاقی |

> BMI is a general screening measure and does not diagnose health conditions.

## 🛠️ Technologies

This project uses:

- **Python 3**
- **Tkinter**
- **Object-Oriented Programming**
- **Classes & Methods**
- **JSON**
- **File Handling**
- **Exception Handling**
- **Conditional Statements**
- **Functions**
- **GUI Development**

## 🧮 BMI Formula

BMI is calculated using the following formula:

```text
BMI = Weight (kg) / Height² (m)
```

For example:

```text
Height = 175 cm
Weight = 70 kg

BMI ≈ 22.9
```

## 🌍 Bilingual Interface

The application supports both **English** and **Persian**.

### English

```text
BMI Calculator

Height: 175 cm
Weight: 70 kg

Your BMI: 22.9
Status: Normal weight
```

### فارسی

```text
محاسبه‌گر شاخص توده بدنی

قد: ۱۷۵ سانتی‌متر
وزن: ۷۰ کیلوگرم

BMI شما: ۲۲٫۹
وضعیت: وزن متعادل
```

The interface changes between **LTR** and **RTL** when the language is switched.

## 💾 Language Preference

The selected language is automatically saved in:

```text
settings.json
```

This file is created automatically after changing the language.

On the next launch, the application loads the previously selected language.

## ⚠️ Input Validation

The application validates user input before calculating BMI.

### Height

```text
50 – 250 cm
```

### Weight

```text
10 – 500 kg
```

Invalid or empty values produce a bilingual error message.

## ⌨️ Keyboard Shortcuts

| Key | Action |
|---|---|
| `Enter` | Calculate BMI |
| `Escape` | Reset |

## ▶️ How to Run

Make sure **Python 3** is installed.

Run:

```bash
python BMI.py
```

On Windows, you can also use:

```bash
py BMI.py
```

No external packages are required because the application uses Python's built-in **Tkinter** library.

## 📁 Project Structure

```text
bmi-calculator/
│
├── BMI.py
├── README.md
└── settings.json
```

> `settings.json` is generated automatically by the application and does not need to be created manually.

## 🎯 Learning Goals

This project was created to practice and improve:

- Python fundamentals
- GUI development with Tkinter
- Classes and Object-Oriented Programming
- Functions and methods
- Conditional statements
- Exception handling
- File handling
- JSON
- Input validation
- Building a complete desktop application
- Creating bilingual user interfaces

## 🚀 Project Status

**Completed** ✅

This is one of my Python learning projects and part of my **Python Projects** collection.

More Python projects will be added to the repository as I continue learning and practicing.

## 👨‍💻 Author

**KeramatNia**

Learning and building with Python 🐍🚀