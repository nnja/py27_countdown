# Python 2.7 Desktop Countdown Timer with PyPortal + CircuitPython

🐍 ✨Python 2.7 will not be maintained after 2020.✨

⏲ Eagerly awaiting Python 2.7's retirement? Use an [Adafruit PyPortal](https://www.adafruit.com/product/4116) to display a countdown timer to the big event on your desktop.

💅 Thirteen themes let you match your countdown timer to your mood. Select your theme by pressing the left and right sides of the touchscreen.

💜 Written by Nina Zakharenko. Stay in touch:

- Twitter - [@nnja](https://twitter.com/nnja)
- Blog - [nnja.io](https://nnja.io)
- [#PythonHardware on Twitter](https://twitter.com/search?f=tweets&q=%23PythonHardware&src=typd)

### 📺 in action!

![in-action](https://user-images.githubusercontent.com/2030983/60445500-4f35ef80-9bed-11e9-93e7-bfa7f2b2e76c.gif)

## Table of Contents

- [About PyPortal and CircuitPython](#about-pyportal-and-circuitpython)
- [About Themes](#about-themes)
- [Dependencies and Libraries](#dependencies-and-libraries)
- [Adding New Fonts and Themes](#adding-new-fonts-and-themes)
- [Contributions and Credits](#contributions-and-credits)

### About PyPortal and CircuitPython

This code is meant to run on a PyPortal.

An [Adafruit PyPortal](https://www.adafruit.com/product/4116) is an wifi-enabled microcontroller device featuring a 3" capacitive touchscreen and CircuitPython baked in.

It can be programmed with [CircuitPython](https://circuitpython.org/), a variant of Python that can be used to program microcontrollers, originally forked from [MicroPython](https://github.com/micropython/micropython).

### About Themes

An `EventTheme` on the PyPortal represents a background, a text color, a font, and label positions for `days`, `hours` and `minutes`.

Switch to the previous theme by pressing on the left side of the touchscreen display, or the next theme by pressing on the right.

Theme backgrounds in 16-bit `.bmp`  (Bitmap Image) format and are located in the `bgs/` directory. Fonts are in `.BDF` (Bitmap Distribution Format) and located in the `fonts/` directory.

Themes are defined in defined at the end of the `themes.py` file. To stop a theme from being displayed, comment out (or delete) the line where it's defined.

Looking for customization? Skip ahead to [adding your own custom themes and fonts](#adding-new-fonts-and-themes).

## Dependencies and Libraries

### Configuring Wifi and Adafruit IO

The PyPortal needs to connect to wifi to fetch the time from the internet using Adafruit IO.

First, rename `secrets.py.sample` to `secrets.py`.

#### Wifi

Update `secrets.py` with the SSID and password for your own wifi network.

Set `ssid` and `password` for your network in the `secrets` dictionary in `secrets.py`.

#### Adafruit IO

If you don't have one already, create a new account on [Adafruit IO](https://io.adafruit.com/).

Set your `aio_username` and `aio_key` in the `secrets` dictionary in `secrets.py`.

**Tip: make sure not to commit your `secrets.py` file to source control.**

### CircuitPython Version

I'm using the new speedier CircuitPython 4.1.0-beta.0 release featuring 2-5x faster code execution and faster display refreshing 🎉.

If you run into issues with the code or the PyPortal, I recommend using the latest stable release, currently [CircuitPython 4.0.1](https://circuitpython.org/board/pyportal/).

### Libraries

For now, use the `adafruit_pyportal.py` library in the `lib` directory of this repository.

The rest of the libraries listed below are compatible with CircuitPython 4.0.1 and are required to be present in the `lib` directory.

[Download the library bundle](https://circuitpython.org/libraries).

 - `adafruit_bus_device`
 - `adafruit_bitmap_font`
 - `adafruit_display_text`
 - `neopixel`
 - `adafruit_pyportal`
 - `adafruit_touchscreen`
 - `adafruit_esp32spi`
 - `adafruit_sdcard`
 - `adafruit_io`

## Adding New Fonts and Themes

### Adding New Fonts

Fonts are located in the `fonts/` directory.

Added fonts must be in `.BDF` file (Bitmap Distribution Format).

Read more about [fonts on the PyPortal](https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display/overview), or review this guide for [converting `.TTF` fonts to `.BDF` format](https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display/conversion).

#### Add the New Font to `Font` constructor

Next, pass the font file-name to the `Fonts` constructor to use it in your themes.

### Adding New Themes

Theme backgrounds are located in the `bgs/` directory.

To display on the PyPortal, background images must be a 16-bit `.bmp` (Bitmap) file.

#### Converting files to 16-bit Bitmap

For quick and easy conversions between image types, use the [ImageMagick](https://imagemagick.org/script/download.php) command line tool by [installing it on your platform](https://imagemagick.org/script/download.php).

First, install the ImageMagick command line tools.

To convert a single file:

```bash
$ convert foo.png BMP2:foo.bmp
```

To convert all the `*.png` files in a directory to 16-bit `*.bmp`, leaving the original images intact:

```bash
$ mogrify -format bmp -define bmp:format=bmp2 -type truecolor *.png
```

#### Add the New Theme to the `ThemeManager`

Make sure the background image and font you'd like to use are in the correct format, and located in the proper directory.

Next, add a new `EventTheme` to the `ThemeManager` constructor at the end of `themes.py`. The minimum information necessary is the background file, the label positions, and the label position axis.

Example:

```python
EventTheme("1-green-and-purple", pos=(60, 155, 260), y_axis=185)
```

Optionally, a font and a font color can be provided as well.

```python
EventTheme("10-bold-black-on-white", pos=(35, 130, 235), y_axis=170, color=0x00000, font="Collegiate-50")
```

*If no font is specified, the default font is used.*

## Contributions and Credits

Have an idea for an improvement? Contributions are welcome. File an issue, or open a pull request.

*Inspired by this [event countdown clock guide](https://learn.adafruit.com/pyportal-event-countdown-clock) by John Park.*