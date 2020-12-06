from flask_login.utils import login_required
from app import app, login_manager
from app.models import *
from app.enums import *
from app.auth import *
from flask import request, jsonify, render_template, session, redirect
from flask_login import login_user, login_required, logout_user


@app.route("/")
def home():
    """
    Placeholder function for documentation of the API
    """
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Placeholder function for documentation of the API
    """

    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username=username).first()

        if not user:
            return "User does not exist!"

        login_user(user, remember=True)

        if "next" in session and session.next is not None:
            return redirect(session["next"])

        return f"<h1>You are logged in as {current_user.username}"

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """
    Placeholder function for documentation of the API
    """
    logout_user()
    return f"<h1>Logged out.</h1>"


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
