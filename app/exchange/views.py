from app import app
from app.models import *
from app.enums import *
from flask import render_template, jsonify, request
from flask_user import login_required, current_user


@app.route("/exchange")
@login_required
def exchange_home():
    """
    Returns homepage for the contract exchange
    """
    contracts = Contract.query.filter(Contract.user_id == current_user.id).all()
    data = ContractSchema(many=True).dump(contracts)

    return render_template("exchange.html", contracts=data)