"""Terminal colors, headings, tables, and reusable input helpers."""
import os
from datetime import datetime

THEMES = {
    "1": {"name": "RETRO HACKER", "green": "\033[92m", "accent": "\033[32m",
          "yellow": "\033[93m", "red": "\033[91m", "cyan": "\033[96m",
          "white": "\033[97m", "muted": "\033[90m", "reset": "\033[0m"},
    "2": {"name": "CLASSIC AMBER", "green": "\033[93m", "accent": "\033[33m",
          "yellow": "\033[97m", "red": "\033[91m", "cyan": "\033[96m",
          "white": "\033[97m", "muted": "\033[90m", "reset": "\033[0m"},
}
current_theme = "1"

def color(key="green"):
    """Return the ANSI color code for the active theme."""
    return THEMES[current_theme].get(key, THEMES[current_theme]["green"])

def set_theme(theme_number):
    """Switch between the two available terminal color themes."""
    global current_theme
    if theme_number in THEMES:
        current_theme = theme_number
        return True
    return False

def clear_screen():
    """Clear the terminal screen when the terminal supports it."""
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    """Wait for the user before returning to a menu."""
    input(f"\n{color('muted')}Press ENTER to continue...{color('reset')}")

def header(title, subtitle=""):
    """Display a consistent retro terminal header."""
    c, r = color("green"), color("reset")
    print(c + "╔" + "═" * 68 + "╗")
    print("║" + title.center(68) + "║")
    print("╚" + "═" * 68 + "╝" + r)
    if subtitle:
        print(f"{color('cyan')}{subtitle}{color('reset')}")
    print(f"{color('muted')}{datetime.now():%A, %B %d, %Y  %I:%M:%S %p}{color('reset')}")
    print()

def line():
    """Print a separator matching the terminal theme."""
    print(color("accent") + "─" * 70 + color("reset"))

def message(text, kind="info"):
    """Print a colored status message."""
    key = {"success": "green", "error": "red", "warning": "yellow",
           "info": "cyan"}.get(kind, "green")
    print(f"{color(key)}{text}{color('reset')}")

def ask(prompt, required=True):
    """Get trimmed text input and reject blank values when required."""
    while True:
        value = input(f"{color('white')}{prompt}{color('reset')}").strip()
        if value or not required:
            return value
        message("This field cannot be blank.", "warning")

def print_table(headers, rows):
    """Display rows in a readable fixed-width terminal table."""
    if not rows:
        message("No records found.", "warning")
        return
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = min(max(widths[index], len(str(value))), 28)
    border = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(color("accent") + border)
    print("|" + "|".join(" " + str(h)[:w].ljust(w) + " " for h, w in zip(headers, widths)) + "|")
    print(border)
    for row in rows:
        cells = []
        for value, width in zip(row, widths):
            value = str(value)
            if len(value) > width:
                value = value[:width - 3] + "..."
            cells.append(" " + value.ljust(width) + " ")
        print("|" + "|".join(cells) + "|")
    print(border + color("reset"))
