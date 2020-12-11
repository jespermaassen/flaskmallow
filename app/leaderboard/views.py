from app import app
from app.models import *
from app.enums import *
from flask import render_template, jsonify, request
from flask_user import login_required, roles_required, current_user
import cryptocompare as cc
from datetime import datetime


@app.route("/leaderboard")
def leaderboard_home():
    """
    Returns homepage for the contract exchange
    """
    users = User.query.order_by(User.money.desc()).all()
    print(users)

    return render_template("leaderboard.html", users=users)
