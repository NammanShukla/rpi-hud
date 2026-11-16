import tkinter as tk
from PIL import Image, ImageTk 

from datetime import datetime
from config.settings import (
    SERVER_REFRESH,
    WEATHER_REFRESH,
    AQI_REFRESH,
    SYSTEM_REFRESH,
    TIMEZONE
)


class Dashboard:

    def __init__(
        self,
        root,
        server_service,
        weather_service,
        air_service,
        system_service
    ):

        self.root = root

        self.server_service = server_service
        self.weather_service = weather_service
        self.air_service = air_service
        self.system_service = system_service

        self.current_theme = {}

        self.build_ui()

    # ---------------------------------
    # UI CONSTRUCTION
    # ---------------------------------

    def build_ui(self):

        self.root.geometry("800x480")
        self.root.title("Server HUD")
        self.root.resizable(False, False)

        self.root.configure(bg="#080A0F")

        self.font_big = ("Monaco", 32, "bold")
        self.font_med = ("Monaco", 16)
        self.font_small = ("Monaco", 12)
        self.font_tiny = ("Monaco", 10)

        # Weather
        self.weather_frame = tk.Frame(self.root)
        self.weather_frame.place(x=15, y=15)

        self.weather_lbl = tk.Label(
            self.weather_frame,
            font=self.font_med,
            justify="left"
        )
        self.weather_lbl.pack(anchor="w")

        # Clock
        self.clock_frame = tk.Frame(self.root)
        self.clock_frame.place(
            relx=0.5,
            y=5,
            anchor="n"
        )

        self.time_lbl = tk.Label(
            self.clock_frame,
            font=self.font_big
        )
        self.time_lbl.pack()

        self.date_lbl = tk.Label(
            self.clock_frame,
            font=self.font_med
        )
        self.date_lbl.pack()

        # Timezones
        self.zones_frame = tk.Frame(self.root)
        self.zones_frame.place(x=650, y=15)

        self.ny_lbl = tk.Label(
            self.zones_frame,
            font=self.font_med
        )
        self.ny_lbl.pack(anchor="e")

        self.sgt_lbl = tk.Label(
            self.zones_frame,
            font=self.font_med
        )
        self.sgt_lbl.pack(anchor="e")

        # Server statistics
        self.server_frame = tk.LabelFrame(
            self.root,
            text=" SERVER ",
            font=self.font_med,
            labelanchor="n"
        )

        self.server_frame.place(
            x=35,
            y=140,
            width=350,
            height=210
        )

        self.status_lbl = tk.Label(
            self.server_frame,
            text="CONNECTING...",
            font=self.font_small
        )
        self.status_lbl.pack(pady=(10, 8))

        self.cpu_lbl = tk.Label(
            self.server_frame,
            text="CPU: --%",
            font=self.font_small
        )
        self.cpu_lbl.pack(anchor="w", padx=15)

        self.cpu_bar = tk.Canvas(
            self.server_frame,
            width=300,
            height=14,
            highlightthickness=0
        )
        self.cpu_bar.pack(pady=(3, 12))

        self.mem_lbl = tk.Label(
            self.server_frame,
            text="RAM: --%",
            font=self.font_small
        )
        self.mem_lbl.pack(anchor="w", padx=15)

        self.mem_bar = tk.Canvas(
            self.server_frame,
            width=300,
            height=14,
            highlightthickness=0
        )
        self.mem_bar.pack(pady=(3, 10))

        # Raspberry Pi statistics
        self.pi_frame = tk.LabelFrame(
            self.root,
            text=" RASPBERRY PI ",
            font=self.font_med,
            labelanchor="n"
        )

        self.pi_frame.place(
            x=415,
            y=140,
            width=350,
            height=105
        )

        self.temp_lbl = tk.Label(
            self.pi_frame,
            text="TEMP: --",
            font=self.font_small
        )
        self.temp_lbl.pack(anchor="w", padx=15, pady=(12, 5))

        self.volt_lbl = tk.Label(
            self.pi_frame,
            text="VOLTAGE: --",
            font=self.font_small
        )
        self.volt_lbl.pack(anchor="w", padx=15)

        # Air Quality
        self.aqi_frame = tk.LabelFrame(
            self.root,
            text=" AIR QUALITY | NEW DELHI ",
            font=self.font_med,
            labelanchor="n"
        )

        self.aqi_frame.place(
            x=415,
            y=260,
            width=350,
            height=150
        )

        self.aqi_lbl = tk.Label(
            self.aqi_frame,
            text="AQI: --",
            font=("Monaco", 18, "bold")
        )
        self.aqi_lbl.pack(anchor="w", padx=15, pady=(10, 5))

        self.pm25_lbl = tk.Label(
            self.aqi_frame,
            text="PM2.5: -- µg/m³",
            font=self.font_tiny
        )
        self.pm25_lbl.pack(anchor="w", padx=15)

        self.pm10_lbl = tk.Label(
            self.aqi_frame,
            text="PM10: -- µg/m³",
            font=self.font_tiny
        )
        self.pm10_lbl.pack(anchor="w", padx=15)

        self.aqi_updated_lbl = tk.Label(
            self.aqi_frame,
            text="Awaiting data...",
            font=self.font_tiny
        )
        self.aqi_updated_lbl.pack(anchor="w", padx=15, pady=(8, 0))

        # Footer
        self.footer_lbl = tk.Label(
            self.root,
            text="– STAY GOLD, SUNSHINE –",
            font=("Monaco", 10, "italic")
        )

        self.footer_lbl.place(
            relx=0.5,
            rely=1.0,
            anchor="s",
            y=-8
        )

        # Collect widgets for theme application
        self.all_frames = [
            self.weather_frame,
            self.clock_frame,
            self.zones_frame
        ]

        self.all_labels = [
            self.weather_lbl,
            self.time_lbl,
            self.date_lbl,
            self.ny_lbl,
            self.sgt_lbl,
            self.status_lbl,
            self.cpu_lbl,
            self.mem_lbl,
            self.temp_lbl,
            self.volt_lbl,
            self.aqi_lbl,
            self.pm25_lbl,
            self.pm10_lbl,
            self.aqi_updated_lbl,
            self.footer_lbl
        ]

        self.all_panels = [
            self.server_frame,
            self.pi_frame,
            self.aqi_frame
        ]

        self.all_canvases = [
            self.cpu_bar,
            self.mem_bar
        ]

    # ---------------------------------
    # THEME APPLICATION
    # ---------------------------------

    def apply_theme(self, theme_name, theme):

        self.current_theme = theme

        bg = theme["background"]
        panel = theme["panel"]
        fg = theme["foreground"]
        muted = theme["muted"]

        self.root.configure(bg=bg)

        for frame in self.all_frames:

            frame.configure(bg=bg)

        for label in self.all_labels:

            label.configure(
                bg=bg,
                fg=fg
            )

        self.footer_lbl.configure(fg=muted)

        for panel_widget in self.all_panels:

            panel_widget.configure(
                bg=panel,
                fg=theme["accent"]
            )

        for label in (
            self.status_lbl,
            self.aqi_lbl
        ):

            label.configure(fg=theme["highlight"])

        for canvas in self.all_canvases:

            canvas.configure(
                bg=panel,
                highlightthickness=0
            )

        self.update_bar(
            self.cpu_bar, 0
        )

        self.update_bar(
            self.mem_bar, 0
        )

        print(f"Theme activated: {theme_name}")

        self.update_theme_icon(theme_name)

    # ---------------------------------
    # PROGRESS BARS
    # ---------------------------------

    def update_bar(self, canvas, percent):

        canvas.delete("all")

        theme = self.current_theme

        if not theme:
            return

        width = 300
        height = 14

        percent = max(0, min(100, float(percent)))

        canvas.create_rectangle(
            0,
            0,
            width,
            height,
            fill=theme["bar_background"],
            outline=""
        )

        canvas.create_rectangle(
            0,
            0,
            width * percent / 100,
            height,
            fill=theme["bar_fill"],
            outline=""
        )

    # ---------------------------------
    # CLOCK
    # ---------------------------------

    def refresh_clock(self):

        now = self.system_service.get_time()

        self.time_lbl.config(
            text=now.strftime("%H:%M:%S")
        )

        day = now.day

        if 11 <= day <= 13:
            suffix = "th"
        else:
            suffix = {
                1: "st",
                2: "nd",
                3: "rd"
            }.get(day % 10, "th")

        self.date_lbl.config(
            text=now.strftime("%B ") + f"{day}{suffix} " + now.strftime("%Y")
        )

        self.ny_lbl.config(
            text="NYC " +
            self.system_service.get_timezone_time(
                "America/New_York"
            )
        )

        self.sgt_lbl.config(
            text="SGT " +
            self.system_service.get_timezone_time(
                "Asia/Singapore"
            )
        )

        self.root.after(1000, self.refresh_clock)

    # ---------------------------------
    # SERVER STATISTICS
    # ---------------------------------

    def refresh_server(self):

        stats = self.server_service.fetch()

        if stats:

            cpu = stats["cpu_percent"]
            ram = stats["ram"]["percent"]

            self.status_lbl.config(
                text="SERVER ONLINE",
                fg=self.current_theme["good"]
            )

            self.cpu_lbl.config(
                text=f"CPU: {cpu}%"
            )

            self.mem_lbl.config(
                text=f"RAM: {ram}%"
            )

            self.update_bar(self.cpu_bar, cpu)
            self.update_bar(self.mem_bar, ram)

        else:

            self.status_lbl.config(
                text="SERVER OFFLINE",
                fg=self.current_theme["danger"]
            )

            self.cpu_lbl.config(text="CPU: --%")
            self.mem_lbl.config(text="RAM: --%")

            self.update_bar(self.cpu_bar, 0)
            self.update_bar(self.mem_bar, 0)

        self.root.after(
            SERVER_REFRESH,
            self.refresh_server
        )

    # ---------------------------------
    # WEATHER
    # ---------------------------------

    def refresh_weather(self):

        data = self.weather_service.fetch()

        if data:

            self.weather_lbl.config(
                text=(
                    f"{data['temperature']:.1f}°C\n"
                    f"{data['description']}"
                )
            )

        else:

            self.weather_lbl.config(
                text="Weather unavailable"
            )

        self.root.after(
            WEATHER_REFRESH,
            self.refresh_weather
        )

    # ---------------------------------
    # AIR QUALITY
    # ---------------------------------

    def refresh_air_quality(self):

        data = self.air_service.fetch()

        if data:

            self.aqi_lbl.config(
                text=(
                    f"AQI: {data['owm_aqi']}/5 "
                    f"({data['aqi_label']})"
                )
            )

            self.pm25_lbl.config(
                text=(
                    f"PM2.5: {data['pm25']} µg/m³"
                    f"  |  Sub-index: {data['pm25_subindex']}"
                )
            )

            self.pm10_lbl.config(
                text=(
                    f"PM10: {data['pm10']} µg/m³"
                    f"  |  Sub-index: {data['pm10_subindex']}"
                )
            )

            updated = datetime.fromtimestamp(
                data["timestamp"]
            )

            self.aqi_updated_lbl.config(
                text=(
                    "Last reading: " +
                    updated.strftime("%H:%M")
                )
            )

        else:

            self.aqi_lbl.config(text="AQI: UNAVAILABLE")
            self.pm25_lbl.config(text="PM2.5: --")
            self.pm10_lbl.config(text="PM10: --")
            self.aqi_updated_lbl.config(text="No data available")

        self.root.after(
            AQI_REFRESH,
            self.refresh_air_quality
        )

    # ---------------------------------
    # PI STATISTICS
    # ---------------------------------

    def refresh_system(self):

        temp = self.system_service.get_pi_temperature()
        volts = self.system_service.get_pi_voltage()

        self.temp_lbl.config(
            text=f"TEMP: {temp}"
        )

        self.volt_lbl.config(
            text=f"VOLTAGE: {volts}"
        )

        self.root.after(
            SYSTEM_REFRESH,
            self.refresh_system
        )

    # ---------------------------------
    # START DASHBOARD
    # ---------------------------------

    def start(self):

        self.refresh_clock()
        self.refresh_server()
        self.refresh_weather()
        self.refresh_air_quality()
        self.refresh_system()


    #---------------------------------
    # ICONS
    #---------------------------------

    def update_theme_icon(self, theme_name):

        icons = {
            "default": "default_edgerunners.png",
            "summer": "summer_sun.png",
            "autumn": "autumn_leaf.png",
            "winter": "winter_snowflake.png",
            "birthday": "birthday_gift.png",
            "halloween": "halloween_pumpkin.png",
            "christmas": "christmas_tree.png",
            "new_year": "new_years_firework.png"
        }

        filename = icons.get(theme_name, "default_edgerunners.png")

        path = f"assets/icons/{filename}"

        image = Image.open(path).convert("RGBA")
        image = image.resize((80, 80), Image.Resampling.LANCZOS)

        self.theme_icon_image = ImageTk.PhotoImage(image)

        if not hasattr(self, "theme_icon_label"):
            self.theme_icon_label = tk.Label(
                self.root,
                bg=self.root["bg"],
                borderwidth=0
            )
            self.theme_icon_label.place(x=130, y=15)

        self.theme_icon_label.configure(image=self.theme_icon_image)