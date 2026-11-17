"""Reports and summaries generated from the TXT databases."""
from students import get_students
from subjects import get_subjects
from grades import get_grades
from interface import print_table, message

def student_report():
    """Print a report showing every registered student."""
    students = get_students()
    print(f"\nSTUDENT RECORDS REPORT | Total students: {len(students)}")
    print_table(["ID", "Name", "Course", "Year"],
                [[s["student_id"], s["first_name"] + " " + s["last_name"],
                  s["course"], s["year_level"]] for s in students])

def academic_report():
    """Print the average grade and academic status for each student with grades."""
    students, grades = get_students(), get_grades()
    rows = []
    for student in students:
        values = [float(g["grade"]) for g in grades
                  if g["student_id"].lower() == student["student_id"].lower()]
        if values:
            average = sum(values) / len(values)
            rows.append([student["student_id"],
                         student["first_name"] + " " + student["last_name"],
                         f"{average:.2f}", "PASSED" if average >= 75 else "NEEDS IMPROVEMENT"])
    print(f"\nACADEMIC PERFORMANCE REPORT | Students with grades: {len(rows)}")
    print_table(["ID", "Student", "Average", "Status"], rows)

def system_summary():
    """Display counts of students, subjects, and grade entries."""
    students, subjects, grades = get_students(), get_subjects(), get_grades()
    print("\nSYSTEM SUMMARY")
    print_table(["Metric", "Total"], [
        ["Registered students", len(students)],
        ["Available subjects", len(subjects)],
        ["Grade entries", len(grades)]
    ])
    if grades:
        average = sum(float(g["grade"]) for g in grades) / len(grades)
        message(f"Overall recorded grade average: {average:.2f}", "success")
