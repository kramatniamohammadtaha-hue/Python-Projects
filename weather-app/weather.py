import threading
import tkinter as tk
from datetime import datetime

import customtkinter as ctk
import requests


class WeatherApp(ctk.CTk):
    """Modern weather application using CustomTkinter and Open-Meteo."""

    API_URL = "https://api.open-meteo.com/v1/forecast"
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

    WEATHER_CODES = {
        0: ("Clear sky", "آسمان صاف", "☀"),
        1: ("Mainly clear", "عمدتاً صاف", "🌤"),
        2: ("Partly cloudy", "نیمه‌ابری", "⛅"),
        3: ("Overcast", "ابری", "☁"),
        45: ("Fog", "مه", "🌫"),
        48: ("Depositing rime fog", "مه یخ‌زن", "🌫"),
        51: ("Light drizzle", "نم‌نم باران", "🌦"),
        53: ("Moderate drizzle", "باران ریز متوسط", "🌦"),
        55: ("Dense drizzle", "باران ریز شدید", "🌧"),
        61: ("Slight rain", "باران کم", "🌦"),
        63: ("Moderate rain", "باران متوسط", "🌧"),
        65: ("Heavy rain", "باران شدید", "🌧"),
        71: ("Slight snow", "برف کم", "🌨"),
        73: ("Moderate snow", "برف متوسط", "❄"),
        75: ("Heavy snow", "برف شدید", "❄"),
        80: ("Rain showers", "رگبار باران", "🌦"),
        81: ("Moderate rain showers", "رگبار متوسط", "🌧"),
        82: ("Violent rain showers", "رگبار شدید", "⛈"),
        95: ("Thunderstorm", "رعدوبرق", "⛈"),
        96: ("Thunderstorm with hail", "رعدوبرق و تگرگ", "⛈"),
        99: ("Thunderstorm with heavy hail", "رعدوبرق و تگرگ شدید", "⛈"),
    }

    TEXT = {
        "en": {
            "title": "Weather App",
            "subtitle": "Real-time weather information powered by Open-Meteo",
            "search": "Search city...",
            "search_button": "Search",
            "refresh": "Refresh",
            "temperature": "Temperature",
            "feels_like": "Feels like",
            "humidity": "Humidity",
            "wind": "Wind",
            "pressure": "Pressure",
            "visibility": "Visibility",
            "sunrise": "Sunrise",
            "sunset": "Sunset",
            "forecast": "5-Day Forecast",
            "language": "فارسی",
            "ready": "Enter a city to get weather information.",
            "loading": "Loading weather data...",
            "not_found": "City not found.",
            "network_error": "Could not connect to the weather service.",
            "api_error": "Weather service returned an error.",
            "invalid": "Please enter a city name.",
            "kmh": "km/h",
            "hpa": "hPa",
            "km": "km",
            "today": "Today",
        },
        "fa": {
            "title": "اپلیکیشن آب‌وهوا",
            "subtitle": "اطلاعات آب‌وهوای لحظه‌ای با Open-Meteo",
            "search": "نام شهر را وارد کنید...",
            "search_button": "جستجو",
            "refresh": "به‌روزرسانی",
            "temperature": "دما",
            "feels_like": "دمای احساس‌شده",
            "humidity": "رطوبت",
            "wind": "باد",
            "pressure": "فشار",
            "visibility": "دید",
            "sunrise": "طلوع",
            "sunset": "غروب",
            "forecast": "پیش‌بینی ۵ روزه",
            "language": "English",
            "ready": "نام یک شهر را وارد کنید تا اطلاعات آب‌وهوا نمایش داده شود.",
            "loading": "در حال دریافت اطلاعات آب‌وهوا...",
            "not_found": "شهر پیدا نشد.",
            "network_error": "اتصال به سرویس آب‌وهوا برقرار نشد.",
            "api_error": "سرویس آب‌وهوا خطا برگرداند.",
            "invalid": "لطفاً نام یک شهر را وارد کنید.",
            "kmh": "کیلومتر/ساعت",
            "hpa": "hPa",
            "km": "کیلومتر",
            "today": "امروز",
        },
    }

    def __init__(self):
        super().__init__()

        self.language = "en"
        self.current_city = ""
        self.current_data = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color="#0b1120")
        self.title("Weather App")
        self.geometry("980x780")
        self.minsize(820, 680)

        self.build_ui()
        self.apply_language()

        self.bind("<Return>", lambda _event: self.search_weather())

    def build_ui(self):
        self.main = ctk.CTkScrollableFrame(
            self, fg_color="transparent", scrollbar_button_color="#273449"
        )
        self.main.pack(fill="both", expand=True, padx=28, pady=24)

        self.header = ctk.CTkFrame(self.main, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.title_label = ctk.CTkLabel(
            self.header, text="", font=ctk.CTkFont(size=30, weight="bold")
        )
        self.title_label.pack()

        self.subtitle_label = ctk.CTkLabel(
            self.header, text="", text_color="#8b98ad",
            font=ctk.CTkFont(size=13)
        )
        self.subtitle_label.pack(pady=(4, 0))

        self.search_frame = ctk.CTkFrame(
            self.main, corner_radius=16, fg_color="#111a2d"
        )
        self.search_frame.pack(fill="x", pady=(0, 18))

        self.search_entry = ctk.CTkEntry(
            self.search_frame, height=46, corner_radius=12,
            border_width=1, border_color="#293750",
            fg_color="#0e1728", font=ctk.CTkFont(size=13)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(14, 8), pady=14)

        self.search_button = ctk.CTkButton(
            self.search_frame, text="", width=110, height=44,
            corner_radius=12, command=self.search_weather,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.search_button.pack(side="left", padx=(0, 8), pady=14)

        self.refresh_button = ctk.CTkButton(
            self.search_frame, text="", width=120, height=44,
            corner_radius=12, fg_color="#263247",
            hover_color="#34425a", command=self.refresh_weather
        )
        self.refresh_button.pack(side="left", padx=(0, 8), pady=14)

        self.language_button = ctk.CTkButton(
            self.search_frame, text="", width=90, height=44,
            corner_radius=12, fg_color="#263247",
            hover_color="#34425a", command=self.toggle_language
        )
        self.language_button.pack(side="left", padx=(0, 14), pady=14)

        self.status_label = ctk.CTkLabel(
            self.main, text="", text_color="#8b98ad",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(0, 10))

        self.current_card = ctk.CTkFrame(
            self.main, corner_radius=20, fg_color="#111a2d",
            border_width=1, border_color="#24334c"
        )
        self.current_card.pack(fill="x", pady=(0, 18))

        self.location_label = ctk.CTkLabel(
            self.current_card, text="—",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.location_label.pack(pady=(22, 2))

        self.country_label = ctk.CTkLabel(
            self.current_card, text="",
            text_color="#7f8da5", font=ctk.CTkFont(size=11)
        )
        self.country_label.pack()

        self.weather_icon = ctk.CTkLabel(
            self.current_card, text="☀", font=ctk.CTkFont(size=58)
        )
        self.weather_icon.pack(pady=(8, 0))

        self.condition_label = ctk.CTkLabel(
            self.current_card, text="—",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.condition_label.pack()

        self.temperature_label = ctk.CTkLabel(
            self.current_card, text="—",
            font=ctk.CTkFont(size=46, weight="bold")
        )
        self.temperature_label.pack(pady=(4, 18))

        self.details = ctk.CTkFrame(self.current_card, fg_color="transparent")
        self.details.pack(fill="x", padx=18, pady=(0, 22))

        self.detail_cards = {}
        for index, key in enumerate(
            ["feels_like", "humidity", "wind", "pressure", "visibility", "sunrise"]
        ):
            card = ctk.CTkFrame(
                self.details, corner_radius=12, fg_color="#182238"
            )
            card.grid(row=index // 3, column=index % 3, sticky="ew", padx=5, pady=5)
            self.details.grid_columnconfigure(index % 3, weight=1)

            title = ctk.CTkLabel(
                card, text="", text_color="#8492aa",
                font=ctk.CTkFont(size=10, weight="bold")
            )
            title.pack(pady=(11, 1))

            value = ctk.CTkLabel(
                card, text="—",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            value.pack(pady=(0, 11))

            self.detail_cards[key] = (title, value)

        self.forecast_title = ctk.CTkLabel(
            self.main, text="",
            font=ctk.CTkFont(size=19, weight="bold")
        )
        self.forecast_title.pack(anchor="w", pady=(0, 10))

        self.forecast_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        self.forecast_frame.pack(fill="x")

    def apply_language(self):
        t = self.TEXT[self.language]

        self.title_label.configure(text=t["title"])
        self.subtitle_label.configure(text=t["subtitle"])
        self.search_entry.configure(placeholder_text=t["search"])
        self.search_button.configure(text=t["search_button"])
        self.refresh_button.configure(text=t["refresh"])
        self.language_button.configure(text=t["language"])
        self.forecast_title.configure(text=t["forecast"])

        if not self.current_data:
            self.status_label.configure(text=t["ready"])

        for key, (title, _value) in self.detail_cards.items():
            title.configure(text=t[key])

        if self.current_data:
            self.render_weather(self.current_data)

    def search_weather(self):
        city = self.search_entry.get().strip()
        if not city:
            self.status_label.configure(text=self.TEXT[self.language]["invalid"])
            return

        self.status_label.configure(text=self.TEXT[self.language]["loading"])
        self.search_button.configure(state="disabled")
        threading.Thread(target=self.fetch_weather, args=(city,), daemon=True).start()

    def refresh_weather(self):
        if self.current_city:
            self.status_label.configure(text=self.TEXT[self.language]["loading"])
            threading.Thread(
                target=self.fetch_weather,
                args=(self.current_city,),
                daemon=True
            ).start()
        else:
            self.search_weather()

    def fetch_weather(self, city):
        try:
            geo_response = requests.get(
                self.GEOCODING_URL,
                params={"name": city, "count": 1, "language": "en", "format": "json"},
                timeout=10,
            )
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            results = geo_data.get("results", [])

            if not results:
                self.after(0, self.show_error, "not_found")
                return

            location = results[0]

            weather_response = requests.get(
                self.API_URL,
                params={
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "current": (
                        "temperature_2m,relative_humidity_2m,apparent_temperature,"
                        "is_day,weather_code,pressure_msl,wind_speed_10m,visibility"
                    ),
                    "daily": "weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset",
                    "timezone": "auto",
                    "forecast_days": 5,
                },
                timeout=10,
            )
            weather_response.raise_for_status()
            weather = weather_response.json()

            data = {"location": location, "weather": weather}
            self.after(0, self.show_weather, data)

        except requests.RequestException:
            self.after(0, self.show_error, "network_error")
        except (ValueError, KeyError):
            self.after(0, self.show_error, "api_error")

    def show_error(self, key):
        self.status_label.configure(text=self.TEXT[self.language][key])
        self.search_button.configure(state="normal")

    def show_weather(self, data):
        self.current_data = data
        self.current_city = data["location"]["name"]
        self.render_weather(data)
        self.search_button.configure(state="normal")

    def render_weather(self, data):
        t = self.TEXT[self.language]
        location = data["location"]
        weather = data["weather"]
        current = weather["current"]
        daily = weather["daily"]

        self.location_label.configure(text=location["name"])
        self.country_label.configure(
            text=f'{location.get("country", "")} • '
                 f'{location["latitude"]:.2f}, {location["longitude"]:.2f}'
        )

        code = current["weather_code"]
        condition = self.WEATHER_CODES.get(code, ("Unknown", "نامشخص", "🌡"))

        if self.language == "fa":
            self.condition_label.configure(text=condition[1])
        else:
            self.condition_label.configure(text=condition[0])

        self.weather_icon.configure(text=condition[2])
        self.temperature_label.configure(
            text=f'{round(current["temperature_2m"])}°C'
        )

        values = {
            "feels_like": f'{round(current["apparent_temperature"])}°C',
            "humidity": f'{current["relative_humidity_2m"]}%',
            "wind": f'{round(current["wind_speed_10m"])} {t["kmh"]}',
            "pressure": f'{round(current["pressure_msl"])} {t["hpa"]}',
            "visibility": f'{round(current["visibility"] / 1000, 1)} {t["km"]}',
            "sunrise": self.format_time(daily["sunrise"][0]),
        }

        for key, value in values.items():
            self.detail_cards[key][1].configure(text=value)

        self.build_forecast(daily)
        self.status_label.configure(text=f'{self.current_city} • {datetime.now():%H:%M}')

    def build_forecast(self, daily):
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        t = self.TEXT[self.language]

        for i in range(5):
            card = ctk.CTkFrame(
                self.forecast_frame, corner_radius=15,
                fg_color="#111a2d", border_width=1,
                border_color="#24334c"
            )
            card.grid(row=0, column=i, sticky="nsew", padx=4)
            self.forecast_frame.grid_columnconfigure(i, weight=1)

            date = datetime.fromisoformat(daily["time"][i])
            day_name = t["today"] if i == 0 else date.strftime("%a")

            code = daily["weather_code"][i]
            condition = self.WEATHER_CODES.get(code, ("Unknown", "نامشخص", "🌡"))
            description = condition[1] if self.language == "fa" else condition[0]

            ctk.CTkLabel(
                card, text=day_name,
                font=ctk.CTkFont(size=11, weight="bold")
            ).pack(pady=(13, 5))

            ctk.CTkLabel(
                card, text=condition[2],
                font=ctk.CTkFont(size=28)
            ).pack()

            ctk.CTkLabel(
                card, text=description,
                wraplength=120,
                text_color="#8b98ad",
                font=ctk.CTkFont(size=9)
            ).pack(pady=5)

            ctk.CTkLabel(
                card,
                text=f'{round(daily["temperature_2m_max"][i])}° / '
                     f'{round(daily["temperature_2m_min"][i])}°',
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(pady=(2, 13))

    @staticmethod
    def format_time(value):
        try:
            return datetime.fromisoformat(value).strftime("%H:%M")
        except ValueError:
            return "—"

    def toggle_language(self):
        self.language = "fa" if self.language == "en" else "en"
        self.apply_language()


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
