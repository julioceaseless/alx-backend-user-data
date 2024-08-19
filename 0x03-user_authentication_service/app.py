#!/usr/bin/env python3
"""Simple flask app"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
print(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """index page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """end-point to register a user"""
    # get form data
    email = request.form['email']
    password = request.form['password']

    # register user
    user = AUTH.register_user(email, password)
    if user is None:
        return jsonify({"message": "email already registered"})
    return jsonify({f"email": email, "message": "user created"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
