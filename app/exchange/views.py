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


@app.route("/close_contract", methods=["GET", "POST"])
@login_required
def close_contract():
    contractId = request.args.get("contractId")
    contract = Contract.query.get(int(contractId))

    # Make sure the contracts belongs to the logged in user
    if contract.user_id != current_user.id:
        return jsonify(result="Unauthorized")

    if contract.status.value != "open":
        return jsonify(result="Contract is not open")

    ASSET = contract.market.split("_")[0].upper()
    CURRENCY = "USD"

    contract.close_price = cc.get_price(ASSET, CURRENCY)[ASSET][CURRENCY]

    if contract.contract_type.value == "long":
        contract.trade_result_pct = (
            contract.close_price - contract.entry_price
        ) / contract.entry_price
    elif contract.contract_type.value == "short":
        contract.trade_result_pct = (
            (contract.close_price - contract.entry_price) / contract.entry_price
        ) * -1

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
    ASSET = request.args.get("market_ticker").split("_")[0].upper()

    user = User.query.get(int(current_user.id))
    position_size = float(request.args.get("position_size"))
    contract_Type = ContractType["long"].value
    market_ticker = request.args.get("market_ticker")

    if position_size > user.money:
        print("Insufficient Funds")
        return jsonify(result="Insufficient Funds")

    new_contract = Contract(
        contract_type=contract_Type,
        market=market_ticker,
        size=position_size,
        entry_price=cc.get_price(ASSET, CURRENCY)[ASSET][CURRENCY],
        user_id=int(current_user.id),
    )

    # Update user's money
    user.money -= new_contract.size

    db.session.add(new_contract)
    db.session.commit()

    return jsonify(result="Succesfully opened contract")


@app.route("/open_contract_short", methods=["GET", "POST"])
@login_required
def open_contract_short():
    CURRENCY = "USD"
    ASSET = request.args.get("market_ticker").split("_")[0].upper()

    user = User.query.get(int(current_user.id))
    position_size = float(request.args.get("position_size"))
    contract_Type = ContractType["long"].value
    market_ticker = request.args.get("market_ticker")

    if position_size > user.money:
        print("Insufficient Funds")
        return jsonify(result="Insufficient Funds")

    new_contract = Contract(
        contract_type=contract_Type,
        market=market_ticker,
        size=position_size,
        entry_price=cc.get_price(ASSET, CURRENCY)[ASSET][CURRENCY],
        user_id=int(current_user.id),
    )
    # Update user's money
    user = User.query.get(int(current_user.id))
    user.money -= new_contract.size

    db.session.add(new_contract)
    db.session.commit()

    return jsonify(result="Succesfully opened contract")
