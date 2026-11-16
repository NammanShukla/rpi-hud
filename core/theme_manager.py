import json
from datetime import datetime
from zoneinfo import ZoneInfo

from config.settings import ( 
    CONFIG_DIR,
    THEMES_DIR,
    TIMEZONE,
    THEME_CHECK_INTERVAL
)


class ThemeManager:

    def __init__(self, on_theme_change):

        self.on_theme_change = on_theme_change
        self.current_theme = None

        self.timezone = ZoneInfo(TIMEZONE)

        self.seasons = self.load_json(
            CONFIG_DIR / "seasons.json"
        )

        self.events = self.load_json(
            CONFIG_DIR / "events.json"
        )

    def load_json(self, path):

        with open(path, "r") as file:
            return json.load(file)

    def is_date_in_range(self, today, start, end):

        current = (today.month, today.day)

        start_month, start_day = map(int, start.split("-"))
        end_month, end_day = map(int, end.split("-"))

        start_date = (start_month, start_day)
        end_date = (end_month, end_day)

        if start_date <= end_date:
            return start_date <= current <= end_date

        # Handles dates spanning December and January
        return current >= start_date or current <= end_date

    def get_active_theme(self):

        today = datetime.now(self.timezone)

        # Check special events first
        for event in self.events["events"]:

            if self.is_date_in_range(
                today,
                event["start"],
                event["end"]
            ):
                return event["name"]

        # Check seasonal themes
        for season in self.seasons["seasons"]:

            if self.is_date_in_range(
                today,
                season["start"],
                season["end"]
            ):
                return season["name"]

        return self.seasons["default"]

    def get_theme_config(self, theme_name):

        path = THEMES_DIR / f"{theme_name}.json"

        if not path.exists():
            path = THEMES_DIR / "default.json"

        return self.load_json(path)

    def refresh(self):

        theme_name = self.get_active_theme()

        if theme_name != self.current_theme:

            theme_config = self.get_theme_config(theme_name)

            self.on_theme_change(theme_name, theme_config)

            self.current_theme = theme_name

        # Recheck periodically
        self.root.after(
            THEME_CHECK_INTERVAL,
            self.refresh
        )

    def start(self, root):

        self.root = root

        # Immediate detection on application startup
        self.refresh()