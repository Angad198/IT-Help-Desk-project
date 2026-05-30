from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey123"
app.config["SESSION_PERMANENT"] = False


# ================= DATABASE =================

def init_db():

    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()

    # Tickets table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_name TEXT,
        issue_title TEXT,
        category TEXT,
        priority TEXT,
        description TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ================= LOGIN PAGE =================

@app.route("/")
def home():
    return render_template("login.html")


# ================= LOGIN VALIDATION =================

@app.route("/login", methods=["POST"])
def login_validation():

    email = request.form.get("email")
    password = request.form.get("password")

    # Demo login
    if email == "admin@helpdesk.com" and password == "admin123":

        session["user"] = email
        return redirect("/dashboard")

    return render_template(
        "login.html",
        error="Invalid Email or Password"
    )


# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    return render_template("dashboard.html")


# ================= CREATE TICKET =================

@app.route("/create-ticket", methods=["GET", "POST"])
def create_ticket():

    if "user" not in session:
        return redirect("/")

    if request.method == "POST":

        employee_name = request.form.get("employee_name")
        issue_title = request.form.get("issue_title")
        category = request.form.get("category")
        priority = request.form.get("priority")
        description = request.form.get("description")

        conn = sqlite3.connect("helpdesk.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tickets (
            employee_name,
            issue_title,
            category,
            priority,
            description,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            employee_name,
            issue_title,
            category,
            priority,
            description,
            "Open"
        ))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("create_ticket.html")

@app.route("/tickets")
def tickets():

    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM tickets
    """)

    all_tickets = cursor.fetchall()

    conn.close()

    return render_template("tickets.html",tickets=all_tickets)


# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect("/")


# ================= RUN APP =================

if __name__ == "__main__":
    app.run(debug=True)