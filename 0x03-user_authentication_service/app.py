#!/usr/bin/env python3
"""Simple flask app"""
from flask import Flask, jsonify, request, make_response, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """index page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """end-point to register a user"""
    # get form data
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # register user
        user = AUTH.register_user(email, password)
        return make_response(jsonify({"email": user.email,
                                      "message": "user created"}))
    except ValueError:
        return make_response(jsonify({"message": "email already registered"}),
                             400)


@app.route("/sessions", methods=['POST'])
def login():
    """login user"""
    # get user data from login form
    email = request.form.get('email')
    password = request.form.get('password')

    # check if credentials are valid
    if not AUTH.valid_login(email, password):
        abort(401)
    # create new session for user
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    # set cookies
    response.set_cookie('session_id', session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
