from flask_login.utils import login_required
from app import app, login_manager
from app.models import *
from app.enums import *
from app.auth import *
from flask import request, jsonify, render_template, session, redirect
from flask_login import login_user, logout_user
from flask_user import login_required


@app.route("/")
def home():
    """
    Placeholder function for documentation of the API
    """
    return render_template("home.html")


@app.route("/login")
def login():
    """
    Placeholder function for documentation of the API
    """
    return render_template("tba.html")


@app.route("/dataview")
@login_required
def dataview_home():
    """
    Placeholder function for documentation of the API
    """
    return render_template("dataview.html")


@app.route("/dataview/contracts")
def display_contracts():
    """
    Placeholder function for documentation of the API
    """
    contracts = Contract.query.all()
    data = ContractSchema(many=True).dump(contracts)
    return render_template("display_contracts.html", contracts=data)


@app.route("/dataview/users")
def display_users():
    """
    Placeholder function for documentation of the API
    """
    users = User.query.all()
    data = UserSchema(many=True).dump(users)

    return render_template("display_users.html", users=data)
