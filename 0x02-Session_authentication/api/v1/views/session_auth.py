#!/usr/bin/env python3
"""
Views for Session Authentication
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models.user import User
import os


@app_views.route("/auth_session/login/", methods=["POST"],
                 strict_slashes=False)
def login():
    """
    Sets Session Authentication for the user

    Returns:
        _type_: _description_
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    response = make_response(jsonify(user.to_json()))
    session_name = os.environ.get("SESSION_NAME")
    response.set_cookie(
        session_name, session_id, httponly=True, secure=True, samesite="Lax"
    )
    return response


@app_views.route("/auth_session/logout/", methods=["DELETE"],
                 strict_slashes=False)
def logout():
    """
    Deletes the user session
    Returns:
        _type_: _description_
    """
    from api.v1.app import auth

    res = auth.destroy_session(request)
    if not res:
        abort(404)
    return {}, 200
