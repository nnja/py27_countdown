"""Calculate time periods, handle PyPortal time update from the internet.

Some methods based on code from this guide by John Park:
learn.adafruit.com/pyportal-event-countdown-clock

Author: Nina Zakharenko
"""
import time

import rtc

from util import log as print


def time_periods_in_epoch(epoch):
    """
    Args:
        epoch (int): the Unix-time epoch to extract time periods from.

    Returns:
        tuple: A tuple of ints (days, hours, mins) in the epoch.
    """
    epoch = epoch // 60
    mins = epoch % 60
    epoch = epoch // 60
    hours = epoch % 24
    epoch = epoch // 24
    days = epoch

    return days, hours, mins


def should_update_time(event_time, last_updated_at_time, update_after_mins=60):
    """
    The clock on the PyPortal drifts, and should be updated
    from the internet periodically for accuracy.

    We want to update the local time when:
    - The local time isn't set
    - After minutes in update_after_mins have passed
    - If the event time hasn't passed

    Args:
        event_time (time.struct_time): Time of the event.
        last_updated_at_time (time.monotonic): Time the local time
            on the PyPortal was last updated from the internet.
        update_after_mins (int, optional): How many minutes to wait
            before updating from the internet again. Defaults to 60.

    Returns:
        bool: If the local device time should be updated from
            the internet.
    """
    just_turned_on = last_updated_at_time is None
    if just_turned_on:
        print("Updating local time: PyPortal just turned on.")
        return True

    time_since_update = time.monotonic() - last_updated_at_time
    is_update_needed = time_since_update > update_after_mins * 60
    if is_update_needed:
        print(
            "Updating local time: last updated {} mins ago.".format(update_after_mins)
        )
        return True

    remaining_time = time.mktime(event_time) - time.mktime(time.localtime())
    is_event_over = remaining_time and remaining_time < 0
    if is_event_over:
        print("Won't update local time: event is over.")
        return False

    return False

def update_local_time_from_internet(pyportal, timezone="Etc/UTC", debug=False):
    """
    Fetches the local time from the internet, and sets it on the PyPortal.

    Make sure you get the local time at the timezone you want, since
    the location set in your secrets file can override this value.

    Set debug to skip fetching time from the internet. Useful for
    faster startup time while reloading code.

    TODO NZ: Figure out why timezone doesn't match https://pythonclock.org/

    Args:
        pyportal (adafruit_pyportal.PyPortal): PyPortal instance.
        timezone (str, optional): Timezone to fetch time from.
            Overwritten by value in secrets.py. Defaults to "Etc/UTC".
        debug (bool, optional): Use the rtc clock time if set.
            Defaults to False.

    Returns:
        float: Monotonic timestamp of the current time.
    """
    is_rtc_clock_set = rtc.RTC().datetime.tm_year != 2000
    if debug and is_rtc_clock_set:
        print("PyPortal local time: Debug mode. Using cached time.")
    else:
        print("PyPortal local time: Trying to update from internet.")
        pyportal.get_local_time(location=timezone, reraise_exceptions=True)

    time_now = time.monotonic()
    print("PyPortal local time: was last updated at", time_now)
    return time_now


def time_remaining(event_time):
    """
    Args:
        event_time (time.struct_time): Time of the event.

    Returns:
        float: Time remaining between now and the event, in
            seconds since epoch.
    """
    now = time.localtime()
    time_remaining = time.mktime(event_time) - time.mktime(now)
    return time_remaining
