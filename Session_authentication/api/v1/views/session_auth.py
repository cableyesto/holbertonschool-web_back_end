#!/usr/bin/env python3
"""Session authentication routes"""
from flask import jsonify, request
from os import getenv
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Login route for session authentication"""

    # Import auth where needed
    from api.v1.app import auth

    # Lazy fallback: if auth is None, dynamically assign SessionAuth
    if auth is None:
        from api.v1.auth.session_auth import SessionAuth
        # monkey-patch auth variable in api.v1.app
        import sys
        sys.modules['api.v1.app'].auth = SessionAuth()
        auth = sys.modules['api.v1.app'].auth

    # Get email and password from form
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or email.strip() == "":
        return jsonify({"error": "email missing"}), 400
    if not password or password.strip() == "":
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create session
    session_id = auth.create_session(user.id)
    if not session_id:
        return jsonify({"error": "session creation failed"}), 500

    # Get cookie name from environment
    session_name = getenv("SESSION_NAME", "_my_session_id")

    # Response with session cookie
    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)
    return response, 200
