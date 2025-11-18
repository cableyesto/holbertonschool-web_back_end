#!/usr/bin/env python3
"""
App module
"""
from flask import Flask, jsonify, request
from auth import Auth
from user import User

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
