from app import app, login_manager
from app.models import *
from app.enums import *
from flask import render_template
from flask_user import login_required, roles_required, current_user


@app.route("/")
def home():
    """
    Home Dir
    """
    return render_template("home.html")


@app.route("/account")
@login_required
def account_home():
    """
    Returns User's account page when logged in
    """
    return render_template("account.html", user=current_user)


@app.route("/account/contracts")
@login_required
def display_contracts():
    """
    Returns Contracts that user opened
    """
    contracts = Contract.query.filter(Contract.user_id == current_user.id).all()
    data = ContractSchema(many=True).dump(contracts)
    return render_template("display_contracts.html", contracts=data)