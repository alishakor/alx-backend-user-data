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
        -index route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def register_user():
    """POST /users
    Return:
        -Register user to database
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login():
    """POST /sessions"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        user_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", user_id)
        return response
    else:
        abort(401)

    @app.route("/sessions", methods=["DELETE"], strict_slashes=False)
    def logout() -> str:
        """DELETE /sessions"""
        session_id = request.cookies.get("session_id")
        user = AUTH.get_user_from_session_id(session_id)
        if user is None:
            abort(403)
        AUTH.destroy_session(user)
        return redirect("/")

    @app.route("/profile", methods=["GET"], strict_slashes=False)
    def profile() -> str:
        """GET /profile"""
        session_id = request.cookies.get("session_id")
        user = AUTH.get_user_from_session_id(session_id)
        if user is None:
            abort(403)
        return jsonify({"email": user.email}), 200

    @app.route('/reset_password', methods=['POST'], strict_slashes=False)
    def get_reset_password_token():
        """reset user password"""
        email = request.form.get('email')
        try:
            token = AUTH.get_reset_password_token(email)
            return jsonify(
                {"email": email, "reset_token": token}), 200
        except ValueError:
            abort(403)

    @app.route('/reset_password', methods=['PUT'], strict_slashes=False)
    def update_password():
        """Updates a user password"""
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
        try:
            if reset_token:
                AUTH.update_password(reset_token, new_password)
                return jsonify({"email": email,
                                "message": "Password updated"}), 200
        except ValueError:
            abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
