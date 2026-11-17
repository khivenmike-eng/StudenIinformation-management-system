"""Main entry point for the Student Information Management System."""
from datetime import datetime
from config import APP_TITLE, APP_VERSION
from storage import ensure_data_files
from authentication import seed_demo_users, login, add_user
from interface import clear_screen, header, line, ask, pause, message, color
from students import add_student, show_students, search_student, update_student, delete_student
from subjects import add_subject, show_subjects, search_subject
from grades import encode_grade, show_grades, student_average
from reports import student_report, academic_report, system_summary
from settings import settings_menu

def student_menu(user):
    """Display student actions and enforce administrator-only editing."""
    while True:
        header("STUDENT MANAGEMENT")
        print("1. Add student")
        print("2. View all students")
        print("3. Search student")
        print("4. Update student")
        print("5. Delete student")
        print("0. Return")
        choice = ask("Choice: ")
        if choice == "1":
            if user["role"] == "Administrator": add_student()
            else: message("Only administrators can add students.", "error")
        elif choice == "2": show_students()
        elif choice == "3": search_student()
        elif choice == "4":
            if user["role"] == "Administrator": update_student()
            else: message("Only administrators can update students.", "error")
        elif choice == "5":
            if user["role"] == "Administrator": delete_student()
            else: message("Only administrators can delete students.", "error")
        elif choice == "0": break
        else: message("Invalid choice.", "error")
        pause()

def subject_menu(user):
    """Display subject catalog actions."""
    while True:
        header("SUBJECT MANAGEMENT")
        print("1. Add subject")
        print("2. View subjects")
        print("3. Search subject")
        print("0. Return")
        choice = ask("Choice: ")
        if choice == "1":
            if user["role"] == "Administrator": add_subject()
            else: message("Only administrators can add subjects.", "error")
        elif choice == "2": show_subjects()
        elif choice == "3": search_subject()
        elif choice == "0": break
        else: message("Invalid choice.", "error")
        pause()

def grade_menu(user):
    """Display grade actions; administrators and staff may encode grades."""
    while True:
        header("GRADE MANAGEMENT")
        print("1. Encode / update grade")
        print("2. View all grades")
        print("3. Calculate student's average")
        print("0. Return")
        choice = ask("Choice: ")
        if choice == "1": encode_grade()
        elif choice == "2": show_grades()
        elif choice == "3": student_average()
        elif choice == "0": break
        else: message("Invalid choice.", "error")
        pause()

def reports_menu():
    """Display available reports and summary options."""
    while True:
        header("REPORTS AND SUMMARIES")
        print("1. Student records report")
        print("2. Academic performance report")
        print("3. Overall system summary")
        print("0. Return")
        choice = ask("Choice: ")
        if choice == "1": student_report()
        elif choice == "2": academic_report()
        elif choice == "3": system_summary()
        elif choice == "0": break
        else: message("Invalid choice.", "error")
        pause()

def dashboard(user):
    """Run the dashboard until the user logs out or exits."""
    while True:
        clear_screen()
        header(APP_TITLE, f"VERSION {APP_VERSION} | LOGGED IN: {user['username']} ({user['role']})")
        line()
        print(" [1] Student Management")
        print(" [2] Subject Management")
        print(" [3] Grade Management")
        print(" [4] Reports and Summaries")
        print(" [5] System Settings")
        if user["role"] == "Administrator":
            print(" [6] Create User Account")
        print(" [L] Logout")
        print(" [0] Exit Application")
        line()
        choice = ask("ENTER COMMAND: ").lower()
        if choice == "1": student_menu(user)
        elif choice == "2": subject_menu(user)
        elif choice == "3": grade_menu(user)
        elif choice == "4": reports_menu()
        elif choice == "5": settings_menu(user)
        elif choice == "6" and user["role"] == "Administrator":
            add_user(); pause()
        elif choice == "l":
            message("You have been logged out.", "success")
            break
        elif choice == "0":
            return False
        else:
            message("Unknown command. Please select a menu option.", "error")
            pause()
    return True

def main():
    """Initialize files, authenticate users, and launch the application."""
    ensure_data_files()
    seed_demo_users()
    while True:
        clear_screen()
        header(APP_TITLE, "A RETRO TERMINAL STUDENT RECORDS CONSOLE")
        print(" [1] LOGIN")
        print(" [0] SHUT DOWN")
        line()
        choice = ask("ENTER COMMAND: ")
        if choice == "0":
            message("System shutdown. Goodbye!", "success")
            break
        elif choice == "1":
            user = login()
            if user:
                if not dashboard(user):
                    break
                pause()
            else:
                pause()
        else:
            message("Invalid command.", "error")
            pause()

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSystem closed safely.")
