from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "horoq_secret_key"

USER = {
    "username": "admin",
    "password": "admin"
}

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    if (
        request.form["username"] == USER["username"]
        and request.form["password"] == USER["password"]
    ):
        session["user"] = USER["username"]
        return redirect("/dashboard")
    return render_template("login.html", error="Invalid credentials")

# ❌ BROKEN ACCESS CONTROL (INTENTIONAL)
@app.route("/dashboard")
def dashboard():
    user = session.get("user", "Guest")
    return render_template("dashboard.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()
