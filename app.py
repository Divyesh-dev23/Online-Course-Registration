from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "course_registration_secret"

DATABASE = "students.db"

# Available courses
courses = [
    "Python Programming",
    "Data Science",
    "Web Development",
    "Machine Learning",
    "Cloud Computing",
    "Cyber Security"
]

# Create database
def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM registrations")
    registrations = cursor.fetchall()

    conn.close()

    return render_template('index.html', registrations=registrations)


# Course registration
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        roll_number = request.form['roll_number']
        email = request.form['email']
        course = request.form['course']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO registrations
            (name, roll_number, email, course)
            VALUES (?, ?, ?, ?)
        """, (name, roll_number, email, course))

        conn.commit()
        conn.close()

        flash("Course registration successful!")

        return redirect(url_for('index'))

    return render_template('register.html', courses=courses)


# Display available courses
@app.route('/courses')
def show_courses():
    return render_template('courses.html', courses=courses)


if __name__ == '__main__':
    create_table()
    app.run(debug=True)
