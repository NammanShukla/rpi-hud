import tkinter as tk
import requests
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv
import subprocess

# CONFIG
SERVER_URL = "http://192.168.0.100:5000/stats"
CITY_NAME = "New Delhi"

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not found in environment variables")

def fetch_stats():
    try:
        response = requests.get(SERVER_URL, timeout=3)
        if response.status_code == 200:
            return response.json()
    except:
        return None
    return None

def fetch_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"{temp:.1f}C\n{desc.title()}"
    except:
        return "Error"
    return "Error"

def get_time(tz):
    return datetime.now(pytz.timezone(tz)).strftime("%H:%M")

def get_temp():
    try:
        out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        return out.strip().split("=")[1]
    except:
        return "--"

def get_volts():
    try:
        out = subprocess.check_output(["vcgencmd", "measure_volts"]).decode()
        return out.strip().split("=")[1]
    except:
        return "--"

def update_bar(canvas, percent):
    canvas.delete("all")
    width = int((percent / 100) * 120)
    canvas.create_rectangle(0, 0, width, 20, fill="lime", outline="black")

def update():
    stats = fetch_stats()
    if stats:
        status_lbl.config(text="SERVER ONLINE", fg="lime")
        cpu_lbl.config(text=f"{stats['cpu_percent']}%")
        update_bar(cpu_bar, stats['cpu_percent'])
        mem_lbl.config(text=f"{stats['ram']['percent']}%")
        update_bar(mem_bar, stats['ram']['percent'])
    else:
        status_lbl.config(text="SERVER OFFLINE", fg="red")
        cpu_lbl.config(text="--%")
        mem_lbl.config(text="--%")
        update_bar(cpu_bar, 0)
        update_bar(mem_bar, 0)

    weather_lbl.config(text=fetch_weather())
    time_lbl.config(text=datetime.now().strftime("%H:%M"))
    date_lbl.config(text=datetime.now().strftime("%dth %B %Y"))
    ny_lbl.config(text=f"NYC {get_time('America/New_York')}")
    sgt_lbl.config(text=f"SGT {get_time('Asia/Singapore')}")
    temp_lbl.config(text=get_temp())
    volt_lbl.config(text=get_volts())

    root.after(5000, update)


root = tk.Tk()
root.geometry("800x480")
root.configure(bg="black")
root.title("Server HUD")
root.resizable(False, False)

# Fonts
font_big = ("Monaco", 28, "bold")
font_med = ("Monaco", 16)
font_small = ("Monaco", 12)

font_date = ("Monaco", 25, "bold")
font_time = ("Monaco", 32, "bold")

font_sidez = ("Monaco", 18)

# Weather Frame
weather_frame = tk.Frame(root, bg="black")
weather_frame.place(x=15, y=10)
weather_lbl = tk.Label(weather_frame, text="", font=font_sidez, fg="white", bg="black")
weather_lbl.pack()

# Time + Date Frame
main_frame = tk.Frame(root, bg="black")
main_frame.place(relx=0.5, y=10, anchor="n")
time_lbl = tk.Label(main_frame, font=font_time, fg="white", bg="black")
time_lbl.pack()
date_lbl = tk.Label(main_frame, font=font_date, fg="white", bg="black")
date_lbl.pack()

# Timezones Frame
zones_frame = tk.Frame(root, bg="black")
zones_frame.place(x=650, y=10)
ny_lbl = tk.Label(zones_frame, font=font_sidez, fg="white", bg="black")
sgt_lbl = tk.Label(zones_frame, font=font_sidez, fg="white", bg="black")
ny_lbl.pack()
sgt_lbl.pack()

# Server Stats Frame
server_frame = tk.LabelFrame(root, text="Server Stats", font=font_med, fg="white", bg="black", labelanchor='n')
server_frame.place(x=50, y=150, width=300, height=250)

status_lbl = tk.Label(server_frame, font=font_small, fg="red", bg="black")
status_lbl.pack(pady=(10, 5))

cpu_text = tk.Label(server_frame, text="CPU:", font=font_small, fg="white", bg="black")
cpu_text.pack(anchor="w", padx=15)
cpu_lbl = tk.Label(server_frame, font=font_small, fg="white", bg="black")
cpu_lbl.pack(anchor="w", padx=15)
cpu_bar = tk.Canvas(server_frame, width=250, height=20, bg="grey")
cpu_bar.pack(pady=(0, 10))

mem_text = tk.Label(server_frame, text="RAM:", font=font_small, fg="white", bg="black")
mem_text.pack(anchor="w", padx=15)
mem_lbl = tk.Label(server_frame, font=font_small, fg="white", bg="black")
mem_lbl.pack(anchor="w", padx=15)
mem_bar = tk.Canvas(server_frame, width=250, height=20, bg="grey")
mem_bar.pack(pady=(0, 10))

# Pi Stats Frame
pi_frame = tk.LabelFrame(root, text="RPI Stats", font=font_med, fg="white", bg="black", labelanchor='n')
pi_frame.place(x=450, y=150, width=300, height=200)

temp_text = tk.Label(pi_frame, text="TEMP:", font=font_small, fg="white", bg="black")
temp_text.pack(anchor="w", padx=15, pady=(10, 0))
temp_lbl = tk.Label(pi_frame, font=font_small, fg="white", bg="black")
temp_lbl.pack(anchor="w", padx=15, pady=(0, 10))

volt_text = tk.Label(pi_frame, text="VOLTS:", font=font_small, fg="white", bg="black")
volt_text.pack(anchor="w", padx=15)
volt_lbl = tk.Label(pi_frame, font=font_small, fg="white", bg="black")
volt_lbl.pack(anchor="w", padx=15, pady=(0, 10))


footer_lbl = tk.Label(root, text="– Made by Namman Shukla –", font=("Monaco", 14, "italic"), fg="#888888", bg="black")
footer_lbl.place(relx=0.5, rely=1.0, anchor="s", y=-10)


# Initial Update
update()
root.mainloop()