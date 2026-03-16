from flask import Flask, render_template, request, jsonify, session, redirect
import json
import os
import uuid

app = Flask(__name__)
app.secret_key = "secret123"

USER_DB = "users.json"
TASK_DB = "tasks.json"


# create files if missing
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

if not os.path.exists(TASK_DB):
    with open(TASK_DB, "w") as f:
        json.dump({}, f)


def load_users():
    with open(USER_DB) as f:
        return json.load(f)


def save_users(data):
    with open(USER_DB, "w") as f:
        json.dump(data, f, indent=4)


def load_tasks():
    with open(TASK_DB) as f:
        return json.load(f)


def save_tasks(data):
    with open(TASK_DB, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")


# REGISTER PAGE
@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():

    data = request.json
    username = data["username"]
    password = data["password"]

    users = load_users()

    if username in users:
        return jsonify({"status":"exists"})

    users[username] = password
    save_users(users)

    return jsonify({"status":"success"})


# LOGIN PAGE
@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data["username"]
    password = data["password"]

    users = load_users()

    if username in users and users[username] == password:
        session["user"] = username
        return jsonify({"status":"success"})

    return jsonify({"status":"fail"})


@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")


# TASK ROUTES
@app.route("/tasks", methods=["GET"])
def get_tasks():

    user = session.get("user")

    tasks = load_tasks()

    return jsonify(tasks.get(user, []))


@app.route("/tasks", methods=["POST"])
def add_task():

    user = session.get("user")

    tasks = load_tasks()

    if user not in tasks:
        tasks[user] = []

    task = {
        "id": str(uuid.uuid4()),
        "title": request.json["title"],
        "completed": False
    }

    tasks[user].append(task)

    save_tasks(tasks)

    return jsonify(task)


@app.route("/tasks/<task_id>", methods=["PUT"])
def toggle_task(task_id):

    user = session.get("user")

    tasks = load_tasks()

    for task in tasks[user]:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]

    save_tasks(tasks)

    return jsonify({"status":"updated"})


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):

    user = session.get("user")

    tasks = load_tasks()

    tasks[user] = [t for t in tasks[user] if t["id"] != task_id]

    save_tasks(tasks)

    return jsonify({"status":"deleted"})


if __name__ == "__main__":
    app.run(debug=True)