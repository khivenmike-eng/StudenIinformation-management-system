"""Student profile management."""
from config import STUDENTS_FILE
from storage import read_records, write_records, append_record
from interface import ask, message, print_table

FIELDS = ["student_id", "first_name", "last_name", "course", "year_level", "email"]

def get_students():
    """Return all student records from students.txt."""
    return read_records(STUDENTS_FILE, FIELDS)

def show_students(records=None):
    """Display student records in a formatted table."""
    records = get_students() if records is None else records
    print_table(["Student ID", "First name", "Last name", "Course", "Year", "Email"],
                [[r["student_id"], r["first_name"], r["last_name"], r["course"],
                  r["year_level"], r["email"]] for r in records])

def add_student():
    """Validate and append a new student profile."""
    records = get_students()
    student_id = ask("Student ID: ")
    if any(r["student_id"].lower() == student_id.lower() for r in records):
        message("Student ID already exists.", "error")
        return
    record = {
        "student_id": student_id,
        "first_name": ask("First name: "),
        "last_name": ask("Last name: "),
        "course": ask("Course / program: "),
        "year_level": ask("Year level (1-4): "),
        "email": ask("Email address: ", required=False)
    }
    if record["year_level"] not in ("1", "2", "3", "4", "5"):
        message("Year level must be from 1 to 5.", "error")
        return
    if append_record(STUDENTS_FILE, FIELDS, record):
        message("Student saved to students.txt.", "success")

def search_student():
    """Search student records by ID, first name, last name, or course."""
    keyword = ask("Search keyword: ").lower()
    matches = [r for r in get_students()
               if keyword in " ".join(r.values()).lower()]
    show_students(matches)

def update_student():
    """Edit an existing student's profile and save the TXT database."""
    records = get_students()
    student_id = ask("Enter student ID to update: ")
    for record in records:
        if record["student_id"].lower() == student_id.lower():
            message("Leave a field blank to keep its current value.")
            for field, label in [("first_name", "First name"),
                                 ("last_name", "Last name"),
                                 ("course", "Course"),
                                 ("year_level", "Year level"),
                                 ("email", "Email")]:
                value = ask(f"{label} [{record[field]}]: ", required=False)
                if value:
                    record[field] = value
            if write_records(STUDENTS_FILE, FIELDS, records):
                message("Student record updated.", "success")
            return
    message("Student ID not found.", "error")

def delete_student():
    """Delete a student after confirmation and remove related grade entries."""
    from grades import remove_grades_for_student
    records = get_students()
    student_id = ask("Student ID to delete: ")
    target = next((r for r in records if r["student_id"].lower() == student_id.lower()), None)
    if not target:
        message("Student ID not found.", "error")
        return
    confirm = ask(f"Delete {target['first_name']} {target['last_name']}? (Y/N): ").lower()
    if confirm == "y":
        records.remove(target)
        if write_records(STUDENTS_FILE, FIELDS, records):
            remove_grades_for_student(student_id)
            message("Student and related grade records deleted.", "success")
    else:
        message("Delete cancelled.", "warning")
