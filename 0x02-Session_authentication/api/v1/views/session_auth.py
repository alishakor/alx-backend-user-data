#!/usr/bin/env python3
"""Module that handles all session authentication route
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """POST api/v1/views/session_auth.py
    Return: json representation of user object
    """
    email = request.form.get('email')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': user_email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_name = getenv("SESSION_NAME")
    response = jsonify(user[0].to_json())
    session_id = auth.create_session(getattr(user[0], 'id'))
    response.set_cookie(session_name, session_id)
    return response


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_session():
    """Deletes a session"""
    from api.v1.app import auth
    deleted_session = auth.destroy_session(request)
    if deleted_session:
        return jsonify({}), 200
    abort(404)
