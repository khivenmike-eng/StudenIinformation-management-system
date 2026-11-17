"""User preferences and account settings."""
from interface import ask, message, THEMES, set_theme, color
from authentication import change_password

def settings_menu(user):
    """Show theme and password settings until the user chooses to return."""
    while True:
        print(f"\n{color('green')}SYSTEM SETTINGS{color('reset')}")
        print("1. Retro Hacker theme (green on black)")
        print("2. Classic Amber theme")
        print("3. Change my password")
        print("0. Return to main menu")
        choice = ask("Select setting: ")
        if choice in ("1", "2"):
            set_theme(choice)
            message(f"Theme changed to {THEMES[choice]['name']}.", "success")
        elif choice == "3":
            change_password(user)
        elif choice == "0":
            break
        else:
            message("Invalid selection.", "error")
