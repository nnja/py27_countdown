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

def display_time_remaining():
    time_remaining = events.time_remaining(event_time)

    if time_remaining < 0:  # The event has passed.
        return False

    days_left, hours_left, mins_left = events.time_periods_in_epoch(time_remaining)
    themes.update_time(days_left, hours_left, mins_left)

    return True

def update_pyportal_local_time_from_internet(updated_at_time):
    if not events.should_update_time(event_time, updated_at_time):
        return updated_at_time

    try:
        just_turned_on = updated_at_time is None
        updated_at_time = events.update_local_time_from_internet(pyportal)
    except RuntimeError as e:
        display_no_wifi(e)
    else:
        # Switch from the loading screen to the countdown screen
        # when PyPortal is just turned on.
        if just_turned_on:
            themes.initialize(pyportal)

        return updated_at_time

def display_event_elapsed():
    print(
        "Event elapsed! Setting event background, "
        "and sleeping for 1 hour.")

    pyportal.set_background("/bgs/final.bmp")

    while True:
        time.sleep(60 * 60)  # Sleep for 1 hour in seconds.

def display_no_wifi(e):
    print(
        "Can't fetch time on PyPortal without a valid WiFi connection. "
        "Sleeping for 1 hour. Error: {}".format(e))

    pyportal.set_background("/bgs/no-wifi.bmp")

    while True:
        time.sleep(60 * 60)  # Sleep for 1 hour in seconds.

last_updated_at_time = None

while True:
    handle_touchscreen()

    last_updated_at_time = update_pyportal_local_time_from_internet(last_updated_at_time)

    if not display_time_remaining():
        display_event_elapsed()