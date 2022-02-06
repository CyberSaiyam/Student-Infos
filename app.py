# Student Information Portal

import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from cs50 import SQL
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

db = SQL("sqlite:///students.db")

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

GENDERS = ['Male','Female','Transgender','Prefer not to say']
MAJORS = ['Biology', 'Economics', 'Business Management', 'History', 'Computer Science', 'Mechanical Engineering', 'Criminal Justice', 'Political Science', 'English', 'Psychology']
YOC = ['Freshman', 'Sophomore', 'Junior', 'Senior']

@app.route('/')
def index():
    STUDENTS = db.execute("select * from students")
    return render_template("index.html",students=STUDENTS)


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        # user_id = session["user_id"]

        Name = request.form.get("studentname")
        Email = request.form.get("email")
        Phone = request.form.get("phonenumber")
        Gender = request.form.get("gender")
        Address = request.form.get("address")
        Department = request.form.get("courseofstudy")
        CollegeYear = request.form.get("yearofstudy")

        # rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure the username was submitted
        if not Name:
            return apology("must provide Name", 400)

        # Ensure email was submitted
        elif not Email:
            return apology("must provide Email", 400)

        elif not Department:
            return apology("must provide a Course Of Study", 400)

        elif not CollegeYear:
            return apology("must provide Year of College", 400)

        else:

            db.execute("INSERT INTO students (Name,Email,Gender,Phone,Address,Department,CollegeYear) VALUES (?,?,?,?,?,?,?) ",Name,Email,Gender,Phone,Address,Department,CollegeYear)
            # Redirect user to home page
            return redirect("/")


    return render_template("add.html", genders=GENDERS, majors=MAJORS,yoc=YOC)


@app.route("/find")
def find():
    return render_template("find.html")

@app.route('/search')
def search():
    name=request.args.get("studentname")
    SEARCH = db.execute("select * from students where Name = ?",name)
    MSG = 'No Record Found'
    return render_template("search.html",students=SEARCH, msg=MSG)

@app.route("/profile/<Id>")
def profile(Id):
    student_id = Id
    PROFILE = db.execute("select * from students where id = ?",student_id)
    return render_template('profile.html',profiles=PROFILE)



@app.route("/edit/<Id>", methods=["GET", "POST"])
def edit(Id):
    student_id = Id
    PROFILE = db.execute("select * from students where id = ?",student_id)

    if request.method == 'POST':
        Name = request.form.get("studentname")
        Email = request.form.get("email")
        Phone = request.form.get("phonenumber")
        Gender = request.form.get("gender")
        Address = request.form.get("address")
        Department = request.form.get("courseofstudy")
        CollegeYear = request.form.get("yearofstudy")

        db.execute("UPDATE students SET Name = ?,Email = ?,Gender = ?,Phone = ?,Address = ?,Department = ?,CollegeYear = ? WHERE Id = ?",
                    Name,Email,Gender,Phone,Address,Department,CollegeYear, student_id)
        return redirect('/')

    return render_template('edit.html',profiles=PROFILE,genders=GENDERS, majors=MAJORS,yoc=YOC)

@app.route("/delete/<Id>")
def delete(Id):
    student_id = Id
    db.execute("delete from students where Id = ?",student_id)
    return redirect('/')


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
