#!/usr/bin/env python3
"""Simple flask app"""
from flask import Flask, jsonify, request, make_response, abort
from flask import redirect, url_for
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


@app.route("/sessions", methods=['DELETE'])
def logout():
    """logs out the user"""
    session_id = request.cookies.get("session_id")
    # get user from session_id
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        # destroy session
        AUTH.destroy_session(user.id)
        return redirect('/')
    # if user does not exist, respond with 403
    return jsonify({}), 403


@app.route("/profile", methods=['GET'])
def profile():
    """view profile"""
    # get session_id from cookies
    session_id = request.cookies.get("session_id")
    print(session_id)
    # get user by session id
    user = AUTH.get_user_from_session_id(session_id)
    print(user)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
