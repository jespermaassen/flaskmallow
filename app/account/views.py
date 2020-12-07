from flask_login.utils import login_required
from app import app, login_manager
from app.models import *
from app.enums import *
from flask import render_template
from flask_user import login_required, roles_required, current_user


@app.route("/")
def home():
    """
    Placeholder function for documentation of the API
    """
    return render_template("home.html")


@app.route("/account")
@login_required
def account_home():
    """
    Placeholder function for documentation of the API
    """
    return render_template("account.html")


@app.route("/account/contracts")
@login_required
def display_contracts():
    """
    Placeholder function for documentation of the API
    """
    contracts = Contract.query.filter(Contract.user_id == current_user.id).all()
    data = ContractSchema(many=True).dump(contracts)
    return render_template("display_contracts.html", contracts=data)


@app.route("/account/users")
def display_users():
    """
    Placeholder function for documentation of the API
    """
    users = User.query.all()
    data = UserSchema(many=True).dump(users)

    return render_template("display_users.html", users=data)
