from flask import Blueprint, render_template, session, abort, request

user = Blueprint("User", __name__)

from application import bcrypt

import os


import models
import jwt


@user.route("/users", methods=["POST"])
def create_user():
    hashed_pw = bcrypt.generate_password_hash(request.json["password"]).decode("utf-8")

    try:
        user = models.User(email=request.json["email"], password=hashed_pw)

        models.db.session.add(user)
        models.db.session.commit()

        encrypted_id = jwt.encode(
            {"user_id": user.id}, os.environ.get("JWT_SECRET"), algorithm="HS256"
        )

        return {"user": user.to_json(), "user_id": encrypted_id}

    except Exception as e:
        return {"error" f"{e}"}, 400


@user.route("/users/login", methods=["POST"])
def login():
    user = models.User.query.filter_by(email=request.json["email"]).first()

    if not user:
        return {"message": "User not found"}

    elif bcrypt.check_password_hash(user.password, request.json["password"]):
        encrypted_id = jwt.encode(
            {"user_id": user.id}, os.environ.get("JWT_SECRET"), algorithm="HS256"
        )
        return {"user": user.to_json(), "user_id": encrypted_id}

    else:
        return {"message": "password incorrect"}


@user.route("/users/verify", methods=["GET"])
def verify_user():
    try:
        print(request.headers["Authorization"])
        decrypted_id = jwt.decode(
            request.headers["Authorization"],
            os.environ.get("JWT_SECRET"),
            algorithms="HS256",
        )["user_id"]

        # print(f'encrypted_id {request.headers["Authorization"]}')
        print(decrypted_id)

        # user = models.User.query.filter_by(id=request.headers["Authorization"]).first()

        user = models.User.query.filter_by(id=decrypted_id).first()

        if user:
            return {"user": user.to_json()}
        else:
            return {"message": "user not found"}, 404

    except Exception as e:
        print(e)
        return {"error" f"{e}"}, 400
