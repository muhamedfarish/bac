from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "horoq_secret_key"

# ❌ Hardcoded admin credentials
USER = {
    "id": "3",
    "username": "admin",
    "password": "admin",
    "role": "admin"
}

# Simulated DB
USERS = {
    "1": {"name": "Farish", "email": "farish@horoq.io", "role": "user"},
    "2": {"name": "Ayaan", "email": "ayaan@horoq.io", "role": "user"},
    "3": {"name": "Admin", "email": "admin@horoq.io", "role": "admin"}
}

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    if request.form["username"] == USER["username"] and request.form["password"] == USER["password"]:
        session["user_id"] = USER["id"]
        session["role"] = USER["role"]
    return redirect("/dashboard")

# ❌ Broken Access Control (intentional)
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/admin")
def admin_panel():
    admin_id = session.get("user_id", "3")
    admin = USERS.get(admin_id)
    return render_template("admin.html", admin=admin, admin_id=admin_id)

# ❌ IDOR
@app.route("/admin/view-profile")
def view_profile():
    user_id = request.args.get("user_id")
    if user_id in USERS:
        return render_template("profile.html", user=USERS[user_id])
    return "Not Found", 404

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
