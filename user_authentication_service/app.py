#!/usr/bin/env python3
"""
App module
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from user import User
from uuid import UUID

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome() -> str:
    """ Welcome route """
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"])
def users() -> str:
    """ Users creation route """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """ Login route """
    email = request.form.get("email")
    password = request.form.get("password")
    is_valid = AUTH.valid_login(email, password)
    if not is_valid:
        abort(401)

    uuid = AUTH.create_session(email)

    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", uuid)
    return res, 200


@app.route("/sessions", methods=["DELETE"])
def logout():
    """ Logout route """
    session_id_request = request.cookies.get('session_id')

    if not session_id_request:
        abort(400)

    user = AUTH.get_user_from_session_id(session_id_request)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile():
    """ Get user profile """
    session_id_request = request.cookies.get('session_id')

    if not session_id_request:
        abort(400)

    try:
        obj = UUID(session_id_request)
    except ValueError:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id_request)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """ Reset password route """
    email = request.form.get("email")
    try:
        uuid = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": uuid}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
