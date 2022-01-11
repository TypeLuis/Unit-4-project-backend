from flask import Blueprint, render_template, session, abort

testing = Blueprint("testing", __name__)


@testing.route("/test", methods=["GET"])
def test():
    return "it works!"


# testing.route("/test", methods=["GET"])(test)
