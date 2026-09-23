from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os


# =========================================================
# APP SETUP
# =========================================================

app = Flask(__name__)

app.secret_key = "ai-practical-hub-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///practicals.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================================================
# DATABASE MODELS
# =========================================================

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


class Practical(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.String(300),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False,
        default="PRACTICAL"
    )

    emoji = db.Column(
        db.String(10),
        nullable=False,
        default="🧪"
    )


# =========================================================
# DATABASE SETUP
# =========================================================

with app.app_context():

    db.create_all()

    # Keep the Practical Hub limited to the
    # six works shown on the dashboard.

    Practical.query.delete()

    practicals = [

        Practical(
            id=1,
            title="Practical 01",
            description="AI laboratory practical — Part 01.",
            category="PRACTICAL",
            emoji="🧪"
        ),

        Practical(
            id=2,
            title="Practical 02",
            description="AI laboratory practical — Part 02.",
            category="PRACTICAL",
            emoji="🧠"
        ),

        Practical(
            id=3,
            title="Practical 03",
            description="AI laboratory practical — Part 03.",
            category="PRACTICAL",
            emoji="⚙️"
        ),

        Practical(
            id=4,
            title="Water Tank Alert",
            description="Smart water monitoring application.",
            category="APPLICATION",
            emoji="💧"
        ),

        Practical(
            id=5,
            title="Loan App",
            description="AI-powered loan application.",
            category="APPLICATION",
            emoji="💰"
        ),

        Practical(
            id=6,
            title="Attendance System",
            description="Student attendance application.",
            category="APPLICATION",
            emoji="👥"
        )

    ]

    db.session.add_all(practicals)

    db.session.commit()


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return redirect(
        url_for("login")
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:

            return """
                <h2>Please enter both
                username and password.</h2>

                <a href="/register">
                    Go Back
                </a>
            """

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            return """
                <h2>Username already registered.</h2>

                <a href="/login">
                    Go to Login
                </a>
            """

        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)

        db.session.commit()

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(
            username=username
        ).first()

        if user and user.password == password:

            session["username"] = user.username

            return redirect(
                url_for("dashboard")
            )

        return """
            <h2>Invalid username
            or password.</h2>

            <a href="/login">
                Try Again
            </a>
        """

    return render_template(
        "login.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "username" not in session:

        return redirect(
            url_for("login")
        )

    practicals = Practical.query.all()

    return render_template(
        "dashboard.html",
        username=session["username"],
        practicals=practicals
    )


# =========================================================
# PRACTICAL PROGRAM FILES
# =========================================================

PROGRAM_FILES = {

    1: "PRACTICAL 1.py",

    2: "PRACTICAL 2A.py",

    3: "PRACTICAL 2B.py",

    4: "Water_Tank_Alert/app.py",

    5: "loan_app/app.py",

    6: "Attendance_Practical5/app.py"


}


# =========================================================
# VIEW PRACTICAL
# =========================================================

@app.route(
    "/practical/<int:practical_id>"
)
def view_practical(practical_id):

    if "username" not in session:

        return redirect(
            url_for("login")
        )

    practical = Practical.query.get_or_404(
        practical_id
    )

    # =====================================================
    # FILES FOR EACH PRACTICAL
    # =====================================================

    practical_files = {

        1: [
            "PRACTICAL 1.py"
        ],

        2: [
            "PRACTICAL 2A.py"
        ],

        3: [
            "PRACTICAL 2B.py"
        ],

        4: [
            "Water_Tank_Alert/app.py",
            "Water_Tank_Alert/Templates/index.html"
        ],

        5: [
            "loan_app/app.py"
        ],

        6: [
            "Attendance_Practical5/app.py",
            "Attendance_Practical5/templates/index.html"
        ]

    }

    project_directory = os.path.dirname(
        app.root_path
    )

    files_to_display = []

    selected_files = practical_files.get(
        practical_id,
        []
    )

    for relative_path in selected_files:

        file_path = os.path.join(
            project_directory,
            *relative_path.split("/")
        )

        if os.path.isfile(file_path):

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                files_to_display.append({

                    "name": relative_path,
                    "content": file.read()

                })

    return render_template(
        "practical.html",
        practical=practical,
        files_to_display=files_to_display
    )

    # =====================================================
    # CONNECT EACH DASHBOARD PRACTICAL
    # TO ITS EXISTING PROGRAM FILE
    # =====================================================

    program_files = {

        1: "PRACTICAL 1.py",

        2: "PRACTICAL 2A.py",

        3: "PRACTICAL 2B.py",

        4: "Water_Tank_Alert/app.py",

        5: "loan_app/app.py",

        6: "Attendance_Practical5/app.py"

    }

    program_code = None

    file_name = program_files.get(
        practical_id
    )

    if file_name:

        # The programs are stored in the
        # main AI-PRACTICALS folder.
        project_directory = os.path.dirname(
            app.root_path
        )

        file_path = os.path.join(
            project_directory,
            *file_name.split("/")
        )

        if os.path.isfile(file_path):

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                program_code = file.read()

        else:

            program_code = (
                "The program file could not be found."
            )

    return render_template(
        "practical.html",
        practical=practical,
        program_code=program_code
    )

# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )