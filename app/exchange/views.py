from app import app
from app.models import *
from app.enums import *
from flask import render_template, jsonify, request
from flask_user import login_required, roles_required, current_user
import cryptocompare as cc
from datetime import datetime


@app.route("/exchange")
@login_required
def exchange_home():
    """
    Returns homepage for the contract exchange
    """
    contracts = Contract.query.filter(Contract.user_id == current_user.id).all()
    data = ContractSchema(many=True).dump(contracts)

    return render_template("exchange.html", contracts=data)


@app.route("/process", methods=["GET", "POST"])
@login_required
def process():
    contractId = request.args.get("contractId")
    contract = Contract.query.get(int(contractId))

    # Make sure the contracts belongs to the logged in user
    if contract.user_id != current_user.id:
        print(
            f"trying to close {contractId} does not belong to user_id {current_user.id}"
        )
        return jsonify(result="Unauthorized")

    if contract.status.value != "open":
        print(f"can only close contracts that are open")
        return jsonify(result="Contract is not open")

    ASSET = contract.market.split("_")[0].upper()
    CURRENCY = "USD"

    contract.close_price = cc.get_price(ASSET, CURRENCY)[ASSET][CURRENCY]

    contract.trade_result_pct = (
        contract.close_price - contract.entry_price
    ) / contract.entry_price
    contract.trade_result_usd = contract.size * contract.trade_result_pct
    contract.status = "closed"
    contract.date_close = datetime.utcnow()

    # Update user's money
    user = User.query.get(int(contract.user_id))
    user.money += contract.trade_result_usd + contract.size

    db.session.commit()

    return jsonify(result="Succesfully closed contract")


@app.route("/open_contract_long", methods=["GET", "POST"])
@login_required
def open_contract_long():
    CURRENCY = "USD"
    ASSET = "BTC"

    new_contract = Contract(
        contract_type=ContractType["long"].value,
        market="btc_usd",
        size=25.0,
        entry_price=cc.get_price(ASSET, CURRENCY)[ASSET][CURRENCY],
        user_id=int(current_user.id),
    )

    # Update user's money
    user = User.query.get(int(current_user.id))
    user.money -= new_contract.size

    db.session.add(new_contract)
    db.session.commit()

    return jsonify(result="Succesfully opened contract")


# Business logic.

# BASIC
# Interface for current pricing (charts)
# Users can open & close Contracts
# When the contract is closed, the trade result is updated in the contract table

# 2.0
# Allow user to set custom expiry dates, stop-loss en take-profits
