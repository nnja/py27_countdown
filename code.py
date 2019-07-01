"""A multi-theme Python 2.7 Countdown Clock for the PyPortal

Author: Nina Zakharenko
"""
import time

import board
from adafruit_pyportal import PyPortal

import events
from themes import themes
from util import touched_sides
from util import log as print  # Alias print to only log while DEBUG is True.


pyportal = PyPortal(status_neopixel=board.NEOPIXEL, default_bg="/bgs/loading.bmp")

time_last_refreshed = None
time_remaining = None

event_time = time.struct_time((2020, 1, 1, 0, 0, 0, None, None, None))
themes.initialize(pyportal)

while True:
    touched_left, touched_right = touched_sides(pyportal.touchscreen)
    if touched_left:
        themes.prev_theme(pyportal)
    elif touched_right:
        themes.next_theme(pyportal)

    if events.should_refresh_time(event_time, time_last_refreshed):
        time_last_refreshed = events.update_local_time_from_internet(
            pyportal, debug=True
        )

    time_remaining = events.time_remaining(event_time)
    days_left, hours_left, mins_left = events.time_periods_in_epoch(time_remaining)
    themes.current_theme.update_time(days_left, hours_left, mins_left)

    if time_remaining < 0:
        print("Event elapsed! Setting event background, sleeping for 1 hour")
        pyportal.set_background("/bgs/final.bmp")
        while True:
            time.sleep(60 * 60)  # 1 hour in seconds.
