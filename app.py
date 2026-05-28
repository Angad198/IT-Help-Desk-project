from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "helpdesksecretkey"


# Login Page
@app.route("/")
def home():
    return render_template("login.html")


# Login Validation
@app.route("/login", methods=["POST"])
def login_validation():

    email = request.form.get("email")
    password = request.form.get("password")

    # Demo credentials
    if email == "admin@helpdesk.com" and password == "admin123":
        session["user"] = email
        return redirect("/dashboard")

    return render_template(
        "login.html",
        error="Invalid Email or Password"
    )


# Dashboard
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    return render_template("dashboard.html")


@app.route("/create-ticket")
def create_ticket():

    if "user" not in session:
        return redirect("/")

    return render_template("create_ticket.html")


# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)