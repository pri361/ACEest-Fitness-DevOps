from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# In-memory application data
members = []
workouts = []


@app.route("/")
def home():
    return render_template(
        "index.html",
        member_count=len(members),
        workout_count=len(workouts)
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/members")
def view_members():
    return render_template("members.html", members=members)


@app.route("/members/add", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":

        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        weight = request.form.get("weight", "").strip()
        goal = request.form.get("goal", "").strip()

        if not name or not age or not weight or not goal:
            return render_template(
                "add_member.html",
                error="All fields are required.",
                form=request.form
            )

        try:
            age = int(age)
            weight = float(weight)
        except ValueError:
            return render_template(
                "add_member.html",
                error="Age must be a whole number and weight must be a number.",
                form=request.form
            )

        if age <= 0 or weight <= 0:
            return render_template(
                "add_member.html",
                error="Age and weight must be greater than zero.",
                form=request.form
            )

        members.append({
            "name": name,
            "age": age,
            "weight": weight,
            "goal": goal
        })

        return redirect(url_for("view_members"))

    return render_template("add_member.html", form={})


@app.route("/workouts")
def view_workouts():
    return render_template("workouts.html", workouts=workouts)


@app.route("/workouts/add", methods=["GET", "POST"])
def add_workout():
    if request.method == "POST":

        name = request.form.get("name", "").strip()
        duration = request.form.get("duration", "").strip()
        calories = request.form.get("calories", "").strip()

        if not name or not duration or not calories:
            return render_template(
                "add_workout.html",
                error="All fields are required.",
                form=request.form
            )

        try:
            duration = int(duration)
            calories = int(calories)
        except ValueError:
            return render_template(
                "add_workout.html",
                error="Duration and calories must be numbers.",
                form=request.form
            )

        if duration <= 0 or calories < 0:
            return render_template(
                "add_workout.html",
                error="Duration must be greater than zero and calories cannot be negative.",
                form=request.form
            )

        workouts.append({
            "name": name,
            "duration": duration,
            "calories": calories
        })

        return redirect(url_for("view_workouts"))

    return render_template("add_workout.html", form={})


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "ACEest Fitness & Gym"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)