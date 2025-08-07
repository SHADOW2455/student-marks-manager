import sqlite3

# Create or connect to database
conn = sqlite3.connect("student_marks.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    marks INTEGER NOT NULL,
    grade TEXT
)
""")
conn.commit()

# Function to calculate grade from marks
def get_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B+"
    elif marks >= 60:
        return "B"
    elif marks >= 50:
        return "C"
    elif marks >= 35:
        return "D"
    else:
        return "F"

# Function to add a new student
def add_student():
    name = input("Enter student name: ")
    try:
        marks = int(input("Enter student marks (out of 100): "))
        if marks < 0 or marks > 100:
            print("Marks should be between 0 and 100.\n")
            return
    except ValueError:
        print("Please enter valid integer marks.\n")
        return

    grade = get_grade(marks)
    cursor.execute("INSERT INTO students (name, marks, grade) VALUES (?, ?, ?)", (name, marks, grade))
    conn.commit()
    print(f" Student added! Grade: {grade}\n")

# View all students
def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    if rows:
        print("\n Student List with Grades:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Marks: {row[2]}, Grade: {row[3]}")
    else:
        print("\n No students found!")
    print()

# Search student by ID
def search_student():
    try:
        student_id = int(input("Enter student ID to search: "))
    except ValueError:
        print("Invalid ID!\n")
        return

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()

    if row:
        print(f"\n Found - ID: {row[0]}, Name: {row[1]}, Marks: {row[2]}, Grade: {row[3]}\n")
    else:
        print("Student not found!\n")

# Update student marks (and grade)
def update_student():
    try:
        student_id = int(input("Enter student ID to update: "))
    except ValueError:
        print("Invalid ID!\n")
        return

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()

    if not row:
        print("Student not found!\n")
        return

    name = input("Enter new name: ")
    try:
        marks = int(input("Enter new marks: "))
        if marks < 0 or marks > 100:
            print("Marks should be between 0 and 100.\n")
            return
    except ValueError:
        print("Invalid marks!\n")
        return

    grade = get_grade(marks)
    cursor.execute("UPDATE students SET name = ?, marks = ?, grade = ? WHERE id = ?", (name, marks, grade, student_id))
    conn.commit()
    print(f"Student updated! New Grade: {grade}\n")

# Delete student
def delete_student():
    try:
        student_id = int(input("Enter student ID to delete: "))
    except ValueError:
        print("Invalid ID!\n")
        return

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()

    if row:
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        print("Student deleted successfully!\n")
    else:
        print("Student not found!\n")

# Main menu
def main():
    while True:
        print("====== Student Marks Management System ======")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by ID")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

# Run the program
if __name__ == "__main__":
    main()

# Close the connection when done
conn.close()