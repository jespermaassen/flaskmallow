from app import app
from app.models import *
from app.enums import *
from flask import request, jsonify


@app.route("/")
def index():
    """
    Placeholder function for documentation of the API
    """
    return "<h1>API DOCUMENTATION</h1>"


@app.route("/api/contracts", methods=["POST"])
def add_contract():
    """
    Creates a single contract, adds it to the database over POST request
    """
    new_contract = Contract(
        user_id=request.json["user_id"],
        entry_price=request.json["entry_price"],
        contract_type=request.json["contract_type"],
        market=request.json["market"],
        size=request.json["size"],
        date_close=request.json["date_close"],
    )

    db.session.add(new_contract)
    db.session.commit()

    return ContractSchema().jsonify((new_contract))


@app.route("/api/contracts", methods=["GET"])
def get_contracts():
    """
    Gets all Contracts in the databse with GET request
    """
    print(app.config)
    all_contracts = Contract.query.all()
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