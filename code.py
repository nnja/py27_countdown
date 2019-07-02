"""A multi-theme Python 2.7 Countdown Clock for the PyPortal

Author: Nina Zakharenko
"""
import time

import board
from adafruit_pyportal import PyPortal

import events
from themes import themes
from util import sides_touched_on
from util import log as print  # Alias print to only log while DEBUG is True.


pyportal = PyPortal(status_neopixel=board.NEOPIXEL, default_bg="/bgs/loading.bmp")
event_time = time.struct_time((2020, 1, 1, 0, 0, 0, None, None, None))

def handle_touchscreen():
    touched_left, touched_right = sides_touched_on(pyportal.touchscreen)

    if touched_left:
        themes.prev_theme(pyportal)
    elif touched_right:
        themes.next_theme(pyportal)

def update_displayed_time_remaining():
    time_remaining = events.time_remaining(event_time)

    days_left, hours_left, mins_left = events.time_periods_in_epoch(time_remaining)
    themes.update_time(days_left, hours_left, mins_left)

    return time_remaining

def display_no_wifi(e):
    pyportal.set_background("/bgs/no-wifi.bmp")

    print(
        "Can't fetch time on PyPortal without a valid Wifi connection. "
        "Sleeping for 1 hour. Error: %s" % e)

    while True:
        time.sleep(60 * 60)  # Sleep for 1 hour in seconds.

def display_event_elapsed():
    pyportal.set_background("/bgs/final.bmp")

    print(
        "Event elapsed! "
        "Setting event background, "
        "sleeping for 1 hour")

    while True:
        time.sleep(60 * 60)  # Sleep for 1 hour in seconds.

time_last_refreshed = None
time_remaining = None

while True:
    handle_touchscreen()

    if events.should_refresh_time(event_time, time_last_refreshed):
        try:
            time_last_refreshed = events.update_local_time_from_internet(pyportal)

            if not themes.current_theme:
                themes.initialize(pyportal)
        except RuntimeError as e:
            display_no_wifi(e)

    if time_remaining and time_remaining < 0:
        display_event_elapsed()
    else:
        time_remaining = update_displayed_time_remaining()
