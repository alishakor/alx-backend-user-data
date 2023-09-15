#!/usr/bin/env python3
"""
basic flask module
"""
from flask import Flask, jsonify, abort, request
from auth import Auth 

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def index():
    """GET /
    Return:
        - index route
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=["POST"], strict_slashes=False)
def register_user():
    """POST /users
    Return: 
        - Register user to database
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)