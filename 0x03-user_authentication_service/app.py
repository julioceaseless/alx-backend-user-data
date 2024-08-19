#!/usr/bin/env python3
"""Simple flask app"""
from flask import Flask, jsonify, request, make_response
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
