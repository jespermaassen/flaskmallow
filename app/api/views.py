from app import app
from app.models import *
from app.enums import *
from flask import request, jsonify, render_template
from flask_user import login_required, current_user
import cryptocompare as cc


@app.route("/api")
def api_home():
    """
    Placeholder function for documentation of the API
    """
    return render_template("api.html")


@app.route("/api/contracts", methods=["GET", "POST"])
@login_required
def add_contract():
    """
    Creates a single contract, adds it to the database over POST request
    """

    action = request.form.get("action")
    print(action)

    if action == "open":
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

        return ContractSchema().jsonify((new_contract))

    elif action == "close":
        # Unpack the query
        contract_id = request.form.get("contractId")

        contract = Contract.query.get(int(contract_id))
        user = User.query.get(int(contract.user_id))
        asset = contract.market.split("_")[0].upper()

        # Check if user owns this contract
        if contract.user_id != current_user.id:
            return jsonify(result="Unauthorized")

        # Check if contract is open
        if contract.status.value != "open":
            return jsonify(result="Contract is not open")

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

        return ContractSchema().jsonify((contract))


@app.route("/api/contracts", methods=["GET"])
def get_contracts():
    """
    Gets all Contracts in the databse with GET request
    With option to specifiy arguments to the query
    """
    all_contracts = Contract.query.filter_by(**request.args.to_dict()).all()

    return jsonify(ContractSchema(many=True).dump(all_contracts))


@app.route("/api/contracts/<id>", methods=["GET"])
def get_contract(id):
    """
    Gets a single Contract in the databse with GET request
    """
    contract = Contract.query.get(id)

    if not contract:
        return jsonify({"message": f"No contract found with id: {id}"})

    return ContractSchema.jsonify(contract)


@app.route("/api/contracts/<id>", methods=["PUT"])
def update_contract(id):
    """
    Update a single Contract in the databse with PUT request
    """
    contract = Contract.query.get(id)

    if not contract:
        return jsonify({"message": f"No contract found with id: {id}"})

    contract.contract_type = request.json["contract_type"]
    contract.size = request.json["size"]
    contract.date_close = request.json["date_close"]
    contract.trade_result = request.json["trade_result"]

    db.session.commit()

    return ContractSchema.jsonify((contract))


@app.route("/api/contracts/<id>", methods=["DELETE"])
def delete_contract(id):
    """
    Delete a Single Contract in the databse with DELETE request
    """
    contract = Contract.query.get(id)

    if not contract:
        return jsonify({"message": f"No contract found with id: {id}"})

    db.session.delete(contract)
    db.session.commit()

    return ContractSchema.jsonify(contract)


def can_post_contract():
    pass