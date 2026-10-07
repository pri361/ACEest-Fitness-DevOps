from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>ACEest Fitness & Gym</h1>
    <p>Welcome to ACEest Fitness & Gym Management System.</p>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)