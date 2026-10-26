from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "student-management-secret-key"

DATABASE = "students.db"


# Connect to the database and create the table
def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Display the dashboard and student records
@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        students=students,
        total_students=total_students
    )


# Add a new student
@app.route("/add", methods=["POST"])
def add_student():
    roll_no = request.form.get("roll_no", "").strip()
    name = request.form.get("name", "").strip()
    course = request.form.get("course", "").strip()
    email = request.form.get("email", "").strip()

    if not all([roll_no, name, course, email]):
        flash("Please fill in all the fields.", "error")
        return redirect("/")

    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                """
                INSERT INTO students (roll_no, name, course, email)
                VALUES (?, ?, ?, ?)
                """,
                (roll_no, name, course, email)
            )

        flash("Student added successfully!", "success")

    except sqlite3.IntegrityError:
        flash("This roll number already exists.", "error")

    return redirect("/")


# Delete a student
@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

    flash("Student deleted successfully!", "success")
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)