import pytest

from app import app, members, workouts


@pytest.fixture
def client():
    app.config["TESTING"] = True

    # Clear in-memory data before each test
    members.clear()
    workouts.clear()

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"ACEest Fitness & Gym" in response.data
    assert b"Fitness Management" in response.data


def test_about_page(client):
    response = client.get("/about")

    assert response.status_code == 200
    assert b"About ACEest Fitness & Gym" in response.data


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"
    assert data["application"] == "ACEest Fitness & Gym"


def test_member_registration(client):
    response = client.post(
        "/members/add",
        data={
            "name": "Rahul Sharma",
            "age": "25",
            "weight": "75.5",
            "goal": "Muscle Gain"
        },
        follow_redirects=False
    )

    assert response.status_code == 302
    assert len(members) == 1
    assert members[0]["name"] == "Rahul Sharma"
    assert members[0]["age"] == 25
    assert members[0]["weight"] == 75.5
    assert members[0]["goal"] == "Muscle Gain"


def test_member_registration_validation(client):
    response = client.post(
        "/members/add",
        data={
            "name": "",
            "age": "25",
            "weight": "75",
            "goal": "Weight Loss"
        }
    )

    assert response.status_code == 200
    assert b"All fields are required." in response.data
    assert len(members) == 0


def test_member_invalid_age(client):
    response = client.post(
        "/members/add",
        data={
            "name": "Rahul Sharma",
            "age": "abc",
            "weight": "75",
            "goal": "Weight Loss"
        }
    )

    assert response.status_code == 200
    assert b"Age must be a whole number" in response.data
    assert len(members) == 0


def test_workout_registration(client):
    response = client.post(
        "/workouts/add",
        data={
            "name": "Treadmill Running",
            "duration": "30",
            "calories": "250"
        },
        follow_redirects=False
    )

    assert response.status_code == 302
    assert len(workouts) == 1
    assert workouts[0]["name"] == "Treadmill Running"
    assert workouts[0]["duration"] == 30
    assert workouts[0]["calories"] == 250


def test_workout_validation(client):
    response = client.post(
        "/workouts/add",
        data={
            "name": "",
            "duration": "30",
            "calories": "250"
        }
    )

    assert response.status_code == 200
    assert b"All fields are required." in response.data
    assert len(workouts) == 0


def test_workout_invalid_duration(client):
    response = client.post(
        "/workouts/add",
        data={
            "name": "Cycling",
            "duration": "-20",
            "calories": "150"
        }
    )

    assert response.status_code == 200
    assert b"Duration must be greater than zero" in response.data
    assert len(workouts) == 0


def test_members_page(client):
    response = client.get("/members")

    assert response.status_code == 200
    assert b"Gym Members" in response.data


def test_workouts_page(client):
    response = client.get("/workouts")

    assert response.status_code == 200
    assert b"Workout Records" in response.data