from app import app
from app.models import *
from app.enums import *
from flask import request, jsonify, render_template
from flask_user import current_user
from flask_user.passwords import verify_password as verify_cred
import cryptocompare as cc
from flask_httpauth import HTTPBasicAuth
from pprint import pprint


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(uname, pword):

    user = User.query.filter(User.username == uname).first()
    if not user:
        return

    hashed_pass = User.query.filter(User.username == uname).first().password
    if verify_cred(user_manager, pword, hashed_pass):
        return user.id


@app.route("/api")
def api_home():
    """
    Placeholder function for documentation of the API
    """
    return render_template("api.html")


# BASIC CRUD OPERATIONS
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

    return jsonify(ContractSchema().dump(contract))


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

    return jsonify(ContractSchema().dump(contract))


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

    return jsonify(ContractSchema().dump(contract))


# TRADING THROUGH API
@app.route("/api/trade/open", methods=["POST"])
@auth.login_required
def api_open_contract():

    # Unpack the query
    user = User.query.get(int(auth.current_user()))

    size = float(request.args.get("size"))
    contract_type = request.args.get("contract_type")
    market_ticker = request.args.get("market")
    asset = market_ticker.split("_")[0].upper()

    # Check if user is trying to open position bigger than current capital
    if size > user.money:
        return jsonify({"message": "Insufficient funds."})

        # Get current asset's price from CryptoCompare
    entry_price = cc.get_price(asset, "USD")[asset]["USD"]

    # Create new contract
    new_contract = Contract(
        user_id=auth.current_user(),
        contract_type=ContractType[contract_type],
        market=market_ticker,
        size=size,
        entry_price=entry_price,
    )

    # Update user's money
    user.money -= new_contract.size

    # Commit the new contract to the database
    db.session.add(new_contract)
    db.session.commit()

    return jsonify(
        code=200, message="success", result=ContractSchema().dump(new_contract)
    )


@app.route("/api/trade/close/<id>")
def api_close_contract():
    # Check if user is logged in and owns this contract
    if current_user.id:
        return jsonify(message="user is logged in")
