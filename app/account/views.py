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
    return render_template("account.html", user=current_user)


@app.route("/account/contracts")
@login_required
def display_contracts():
    """
    Placeholder function for documentation of the API
    """
    contracts = Contract.query.filter(Contract.user_id == current_user.id).all()
    data = ContractSchema(many=True).dump(contracts)
    return render_template("display_contracts.html", contracts=data)