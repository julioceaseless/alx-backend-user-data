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
    # get user by session id
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """reset password"""
    # get user email
    email = request.form.get("email")
    # get reset token or catch error if email does not exist
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("reset_password", methods=["PUT"])
def update_password():
    """update password form"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({{"email": email,
                         "message": "Password updated"}}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
