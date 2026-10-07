from flask import Flask, request, redirect, url_for

app = Flask(__name__)

members = []
workouts = []


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ACEest Fitness & Gym</title>
    </head>
    <body>
        <h1>ACEest Fitness & Gym</h1>
        <h2>Fitness & Gym Management System</h2>

        <p>Welcome to ACEest Fitness & Gym.</p>

        <h3>Management Options</h3>

        <ul>
            <li><a href="/members">View Members</a></li>
            <li><a href="/members/add">Register Member</a></li>
            <li><a href="/workouts">View Workouts</a></li>
            <li><a href="/workouts/add">Add Workout</a></li>
            <li><a href="/about">About ACEest</a></li>
        </ul>
    </body>
    </html>
    """


@app.route("/about")
def about():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>About - ACEest Fitness & Gym</title>
    </head>
    <body>
        <h1>About ACEest Fitness & Gym</h1>

        <p>
            ACEest Fitness & Gym is a simple fitness management
            application developed as part of a DevOps project.
        </p>

        <a href="/">Home</a>
    </body>
    </html>
    """


@app.route("/members")
def view_members():
    member_list = ""

    if members:
        for member in members:
            member_list += f"""
            <li>
                {member['name']} -
                Age: {member['age']} -
                Weight: {member['weight']} kg -
                Goal: {member['goal']}
            </li>
            """
    else:
        member_list = "<li>No members registered yet.</li>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Members - ACEest Fitness & Gym</title>
    </head>
    <body>
        <h1>Gym Members</h1>

        <ul>
            {member_list}
        </ul>

        <a href="/members/add">Register New Member</a>
        <br>
        <a href="/">Home</a>
    </body>
    </html>
    """


@app.route("/members/add", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        member = {
            "name": request.form.get("name"),
            "age": request.form.get("age"),
            "weight": request.form.get("weight"),
            "goal": request.form.get("goal")
        }

        members.append(member)

        return redirect(url_for("view_members"))

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Member - ACEest Fitness & Gym</title>
    </head>
    <body>
        <h1>Register New Member</h1>

        <form method="POST">

            <label>Name:</label><br>
            <input type="text" name="name" required><br><br>

            <label>Age:</label><br>
            <input type="number" name="age" required><br><br>

            <label>Weight (kg):</label><br>
            <input type="number" step="0.1" name="weight" required><br><br>

            <label>Fitness Goal:</label><br>
            <input type="text" name="goal" required><br><br>

            <button type="submit">Register Member</button>

        </form>

        <br>
        <a href="/">Home</a>
    </body>
    </html>
    """


@app.route("/workouts")
def view_workouts():
    workout_list = ""

    if workouts:
        for workout in workouts:
            workout_list += f"""
            <li>
                {workout['name']} -
                Duration: {workout['duration']} minutes -
                Calories: {workout['calories']}
            </li>
            """
    else:
        workout_list = "<li>No workouts recorded yet.</li>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Workouts - ACEest Fitness & Gym</title>
    </head>
    <body>
        <h1>Workout Records</h1>

        <ul>
            {workout_list}
        </ul>

        <a href="/workouts/add">Add Workout</a>
        <br>
        <a href="/">Home</a>
    </body>
    </html>
    """


@app.route("/workouts/add", methods=["GET", "POST"])
def add_workout():
    if request.method == "POST":
        workout = {
            "name": request.form.get("name"),
            "duration": request.form.get("duration"),
            "calories": request.form.get("calories")
        }

        workouts.append(workout)

        return redirect(url_for("view_workouts"))

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Workout - ACEest Fitness & Gym</title>
    </head>
    <body>
        <h1>Add Workout</h1>

        <form method="POST">

            <label>Workout Name:</label><br>
            <input type="text" name="name" required><br><br>

            <label>Duration (minutes):</label><br>
            <input type="number" name="duration" required><br><br>

            <label>Calories Burned:</label><br>
            <input type="number" name="calories" required><br><br>

            <button type="submit">Add Workout</button>

        </form>

        <br>
        <a href="/">Home</a>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)