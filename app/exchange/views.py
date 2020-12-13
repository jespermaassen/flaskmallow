from app import app
from app.models import *
from app.enums import *
from flask import render_template, jsonify, request
from flask_user import login_required, current_user
import cryptocompare as cc


@app.route("/exchange")
@login_required
def exchange_home():
    """
    Returns homepage for the contract exchange
    """
    contracts = Contract.query.filter(Contract.user_id == current_user.id).all()
    data = ContractSchema(many=True).dump(contracts)

    return render_template("exchange.html", contracts=data)


@app.route("/exchange/open", methods=["POST"])
@login_required
def open_contract():
    """
    Creates a single contract, adds it to the database over POST request
    """

    # Unpack the query
    user = User.query.get(int(current_user.id))
    size = float(request.form.get("size"))
    contract_type = request.form.get("contract_type")
    market_ticker = request.form.get("market")
    asset = market_ticker.split("_")[0].upper()

    # Check if user is trying to open position bigger than current capital
    if size > user.money:
        return jsonify({"message": "Insufficient funds."})

    # Get current asset's price from CryptoCompare
    entry_price = cc.get_price(asset, "USD")[asset]["USD"]

    # Create new contract
    new_contract = Contract(
        user_id=current_user.id,
        contract_type=contract_type,
        market=market_ticker,
        size=size,
        entry_price=entry_price,
    )

    # Update user's money
    user.money -= new_contract.size

    # Commit the new contract to the database
    db.session.add(new_contract)
    db.session.commit()

    return jsonify(code=200, message="success")


@app.route("/exchange/close", methods=["POST"])
@login_required
def close_contract():
    # Unpack the query
    contract_id = request.form.get("contractId")

    contract = Contract.query.get(int(contract_id))
    user = User.query.get(int(contract.user_id))
    asset = contract.market.split("_")[0].upper()

    # Check if user owns this contract
    if contract.user_id != current_user.id:
        return jsonify(message="Unauthorized")

    # Check if contract is open
    if contract.status.value != "open":
        return jsonify(message="Contract is not open")

    # Update the contract
    contract.close_price = cc.get_price(asset, "USD")[asset]["USD"]
    if contract.contract_type.value == "long":
        contract.trade_result_pct = (
            contract.close_price - contract.entry_price
        ) / contract.entry_price
    elif contract.contract_type.value == "short":
        contract.trade_result_pct = (
            (contract.close_price - contract.entry_price) / contract.entry_price
        ) * -1
    contract.trade_result_usd = contract.size * contract.trade_result_pct
    contract.status = ContractStatus["closed"]
    contract.date_close = datetime.utcnow()

    # Update user's money
    user.money += contract.trade_result_usd + contract.size

    db.session.commit()

    return jsonify(code=200, message="success")
