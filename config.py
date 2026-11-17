"""Shared paths and application settings."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "users.txt"
STUDENTS_FILE = DATA_DIR / "students.txt"
SUBJECTS_FILE = DATA_DIR / "subjects.txt"
GRADES_FILE = DATA_DIR / "grades.txt"

APP_TITLE = "STUDENT INFORMATION MANAGEMENT SYSTEM"
APP_VERSION = "1.0"
