"""Utility methods for logging and touchscreen handling

Author: Nina Zakharenko
"""

import time

DEBUG = True


def log(*args):
    """
    Helper method that only prints if the DEBUG
    flag is set to True.

    To use, override the builtin print:
        from util import log as print

    Otherwise:
        from util import log
        log("string")
    """
    if DEBUG:
        print("LOG:", *args)


def get_last_touched_point(touchscreen):
    """
    Return the last known point touched on the
    touchscreen after no more touch events are detected.

    This helps prevent phantom touches from being registered
    when the touchscreen is being pressed on continuously.

    Args:
        touchscreen (adafruit_touchscreen.Touchscreen): An
        instantiated touchscreen object. i.e. if using a
        PyPortal, pyportal.touchscreen.

    Returns:
        A tuple of x, y coordinates of the last touched point,
        or None if no touched point was detected.
    """
    touch_point = touchscreen.touch_point

    if not touch_point:
        return None

    while touch_point:
        latest_touch_point = touchscreen.touch_point
        if not latest_touch_point:
            break
        touch_point = latest_touch_point

    log("Touched at point:", touch_point)
    time.sleep(0.1)

    return touch_point


def touched_sides(touchscreen, left_x_boundary=110, right_x_boundary=240):
    """
    Given a Touchscreen instance, determine if either the
    left or the right side of the screen was touched.

    Args:
        touchscreen (adafruit_touchscreen.Touchscreen): Touchscreen
            instance
        left_x_boundary (int, optional): x boundary for left side of the
            screen. Defaults to 110
        right_x_boundary (int, optional): x boundary for right side of the
            screen. Defaults to 240

    Returns:
        tuple: A tuple with two boolean values, marking if the left, right, or
        neither side was touched.
    """
    touch_point = get_last_touched_point(touchscreen)

    if not touch_point:
        return (False, False)

    touch_x, _, _ = touch_point
    touched_left = touch_x < left_x_boundary
    touched_right = touch_x > right_x_boundary

    return touched_left, touched_right
