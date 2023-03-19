import pytest
from flask import Flask, g, session
from flask.testing import FlaskClient

from flaskr.db import get_db

# register users


def test_register(client: FlaskClient, app: Flask):
    """Checks that registers is a page and that you can register this user"""
    assert client.get("/register").status_code == 200

    with app.app_context():
        form = {
            "username": "ab",
            "email": "testregister@maybe",
            "confirm": "a",
            "password": "a",
            "submit": True,
        }

        response = client.post(
            "/register",
            data=form,
        )

    assert response.headers.get("Location") == "/login"

    with app.app_context():
        assert (
            get_db()
            .execute(
                "SELECT * FROM user WHERE username = 'ab'",
            )
            .fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "email", "password"),
    (
        ("", "", ""),
        ("test", "a@a", ""),
        ("test", "a@a", "a"),
    ),
)
def test_register_validate_input(client, username, email, password):
    """Checks that registers doesn't work with missing arugments or when someone is registering a username/email already used"""
    response = client.post(
        "/register",
        data={
            "username": username,
            "email": email,
            "password": password,
            "confirm": password,
            "submit": "Register",
        },
    )
    assert b"Join Today" in response.data


# user login


def test_login(client, auth):
    assert client.get("login").status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/home"

    with client:
        client.get("/home")
        assert session["user_id"] == 1
        assert g.user["username"] == "test"


@pytest.mark.parametrize(
    ("email", "password", "message"),
    (
        ("a@b", "test", b"Incorrect email."),
        ("a@a", "a", b"Incorrect password."),
    ),
)
def test_login_validate_input(auth, email, password, message):
    response = auth.login(email, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session


# test admin login
def test_admin_login(client, auth):
    """check that you can log in with admin credentials and that there is a table inside it"""
    response = client.post(
        "/login", data={"email": "admin@a", "password": "admin", "submit": True}
    )

    assert response.headers.get("Location") == "/home"
    response = client.get(response.headers.get("Location"))

    assert b"table" in response.data
