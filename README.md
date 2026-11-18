# Student Information System

**Python Final Laboratory Project: Terminal-Based Management System with File Handling**

## 1. Project description
The Student Information System is a menu-driven, terminal-based application for managing student profiles, subjects, and grades. It uses plain-text `.txt` files for storage and provides role-based login, reports, input validation, and two terminal color themes.

## 2. Features
- Administrator and Staff login roles
- Passwords stored as salted SHA-256 hashes (not plain text)
- Student add, view, and search
- Subject add (Administrator only) and view
- Grade encoding with validation (0 to 100)
- Student report card and class summary
- Two color themes (Green and Cyan)
- Password change
- Data remains saved after closing and reopening the program

## 3. Requirements
- Python 3.9 or later
- Terminal / command prompt
- No third-party packages are required

## 4. Installation and running
1. Download or clone this repository.
2. Open a terminal in the `Student-Information-System` folder.
3. Run:

   ```bash
   python main.py
   ```

   On some systems, use `python3 main.py`.

The program automatically creates missing `.txt` files when it starts.

## 5. Demo accounts
The first run creates these sample accounts only when `users.txt` is empty:

| Role | Username | Initial password |
|---|---|---|
| Administrator | `admin` | `admin123` |
| Staff | `staff` | `staff123` |

**Security reminder:** These are demonstration credentials only. The `users.txt` file stores salted password hashes, not readable passwords. Do not upload real passwords or sensitive personal information to a public repository.

## 6. Text database format
Fields are separated by the pipe character (`|`).

- `users.txt`: username, salt, password hash, role
- `students.txt`: student ID, full name, course, year level
- `subjects.txt`: subject code, subject title, units
- `grades.txt`: student ID, subject code, grade

The program reads records when a menu option is used and writes changes back to the text files. Avoid typing the `|` character in field values because it is the field separator.

## 7. Role permissions
- **Administrator:** all features, including adding subjects.
- **Staff:** add, view, and search students, view subjects, add grades, view reports, change theme, and change own password. Staff cannot add subjects.

## 8. Reports
1. **Student Report Card:** shows one student's subjects, grades, and average.
2. **Class Summary:** shows each student's average with a Passed or Failed status, the number of graded students, how many passed, and the top student.

The passing grade of 75 is a sample rule and can be changed in `main.py`.

## 9. Demonstration sequence
1. Run `main.py` and show the login screen.
2. Log in as Administrator and show the main dashboard.
3. Add a student and view the student list.
4. Search for a student by ID or name.
5. Add a subject and view the subject list.
6. Add a grade for a student.
7. Open the Report Card and Class Summary.
8. Change the color theme.
9. Change the password.
10. Log out and run the program again to show that records are saved.

## 10. Screenshots

### Login
![Login](screenshots/login.png)

### Main Dashboard
![Main Dashboard](screenshots/Main%20dashboard.png)

### Add Student
![Add Student](screenshots/Add%20student.png)

### View Subjects
![View Subjects](screenshots/View%20subjects.png)

### Add Grade
![Add Grade](screenshots/Add%20grade.png)

### Student Report Card
![Student Report Card](screenshots/Student%20report%20card.png)

### Class Summary
![Class Summary](screenshots/Class%20summary.png)

### Theme Customization
![Theme](screenshots/Theme.png)

## 11. Files
- `main.py`
- `users.txt`
- `students.txt`
- `subjects.txt`
- `grades.txt`
- `screenshots/`

## 12. Limitations / notes
- This is an educational local terminal project, not a production student-record platform.
- The text files are not encrypted and do not support multi-user file locking.
- ANSI colors work in most modern terminals. If colors do not display, use a terminal that supports ANSI escape codes.

## 13. Author
Banua, Shekyla S.
BSCS 2nd Year-A
