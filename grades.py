"""Grade encoding, viewing, and student grade calculations."""
from config import GRADES_FILE
from storage import read_records, write_records, append_record
from interface import ask, message, print_table
from students import get_students
from subjects import get_subjects

FIELDS = ["student_id", "subject_code", "grade", "semester"]

def get_grades():
    """Load all grade entries from grades.txt."""
    return read_records(GRADES_FILE, FIELDS)

def encode_grade():
    """Record a student's grade after validating the student and subject."""
    student_id = ask("Student ID: ")
    if not any(s["student_id"].lower() == student_id.lower() for s in get_students()):
        message("Student does not exist. Add the student first.", "error")
        return
    subject_code = ask("Subject code: ").upper()
    if not any(s["subject_code"].upper() == subject_code for s in get_subjects()):
        message("Subject does not exist. Add the subject first.", "error")
        return
    try:
        grade = float(ask("Grade (0-100): "))
        if not 0 <= grade <= 100:
            raise ValueError
    except ValueError:
        message("Grade must be a number from 0 to 100.", "error")
        return
    semester = ask("Semester (e.g. 1st Semester): ")
    entries = get_grades()
    entries = [g for g in entries if not (
        g["student_id"].lower() == student_id.lower()
        and g["subject_code"].upper() == subject_code
        and g["semester"].lower() == semester.lower())]
    entries.append({"student_id": student_id, "subject_code": subject_code,
                    "grade": f"{grade:.2f}", "semester": semester})
    if write_records(GRADES_FILE, FIELDS, entries):
        message("Grade saved. Existing same-subject/semester grade was replaced.", "success")

def show_grades():
    """Display all saved grade entries."""
    print_table(["Student ID", "Subject", "Grade", "Semester"],
                [[g["student_id"], g["subject_code"], g["grade"], g["semester"]]
                 for g in get_grades()])

def student_average():
    """Calculate and display the average grade for one student."""
    student_id = ask("Student ID: ")
    grades = [float(g["grade"]) for g in get_grades()
              if g["student_id"].lower() == student_id.lower()]
    if not grades:
        message("No grades found for that student.", "warning")
        return
    average = sum(grades) / len(grades)
    status = "PASSED" if average >= 75 else "NEEDS IMPROVEMENT"
    message(f"Average: {average:.2f} | Result: {status}", "success" if average >= 75 else "warning")

def remove_grades_for_student(student_id):
    """Remove grade entries belonging to a deleted student."""
    records = [g for g in get_grades() if g["student_id"].lower() != student_id.lower()]
    write_records(GRADES_FILE, FIELDS, records)
