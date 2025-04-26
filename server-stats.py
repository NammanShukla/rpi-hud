import tkinter as tk
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# CONFIG
SERVER_URL = "http://192.168.0.100:5000/stats"    
CITY_NAME = "New Delhi"

load_dotenv()
OPENWEATHER_API_KEY= os.getenv("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not found in environment variables")

def fetch_stats():
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching server stats: {e}")
    return None

def fetch_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"{temp}°C, {description.capitalize()}"
    except Exception as e:
        print(f"Error fetching weather: {e}")
    return "Error Fetching Results"

def update_data():
    stats = fetch_stats()
    if stats:
         cpu_label.config(text=f"CPU: {stats['cpu_percent']}%")

         mem_used = int(stats['ram']['used']) // (1024 * 1024)
         mem_total = int(stats['ram']['total']) // (1024 * 1024)
         mem_percent = stats['ram']['percent']
         mem_label.config(text=f"Memory: {mem_used} MB / {mem_total} MB ({mem_percent}%)")

    weather = fetch_weather()
    weather_label.config(text=f"Weather: {weather}")

    now = datetime.now()
    time_label.config(text=now.strftime("%d %b %Y | %H:%M"))

    root.after(5000, update_data)  

# GUI Setup
root = tk.Tk()
root.title("Server HUD")
root.geometry("320x480")  
root.configure(bg="black")

font_big = ("Helvetica", 18, "bold")
font_small = ("Helvetica", 14)

time_label = tk.Label(root, font=font_big, fg="lime", bg="black")
time_label.pack(pady=10)

weather_label = tk.Label(root, font=font_small, fg="cyan", bg="black")
weather_label.pack(pady=5)

cpu_label = tk.Label(root, font=font_small, fg="white", bg="black")
cpu_label.pack(pady=5)

mem_label = tk.Label(root, font=font_small, fg="white", bg="black")
mem_label.pack(pady=5)

update_data()

root.mainloop()
