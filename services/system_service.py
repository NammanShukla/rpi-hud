import subprocess

from datetime import datetime
from zoneinfo import ZoneInfo

from config.settings import TIMEZONE


class SystemService:

    def get_time(self):

        return datetime.now(
            ZoneInfo(TIMEZONE)
        )

    def get_timezone_time(self, timezone):

        return datetime.now(
            ZoneInfo(timezone)
        ).strftime("%H:%M")

    def get_pi_temperature(self):

        try:

            result = subprocess.check_output(
                ["vcgencmd", "measure_temp"],
                text=True,
                timeout=2
            )

            return result.strip().split("=")[1]

        except (subprocess.SubprocessError, OSError, IndexError):
            return "--"

    def get_pi_voltage(self):

        try:

            result = subprocess.check_output(
                ["vcgencmd", "measure_volts"],
                text=True,
                timeout=2
            )

            return result.strip().split("=")[1]

        except (subprocess.SubprocessError, OSError, IndexError):
            return "--"