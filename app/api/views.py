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


@app.route("/api/trade")
def api_open_contract():
    return jsonify(message="this is a test")


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