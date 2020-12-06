from app import app
from app.models import *
from app.enums import *
from flask import request, jsonify, render_template


@app.route("/")
def home():
    """
    Placeholder function for documentation of the API
    """
    return render_template("home.html")


@app.route("/dataview")
def dataview_home():
    """
    Placeholder function for documentation of the API
    """
    return render_template("dataview.html")


@app.route("/dataview/contracts")
def display_contracts():
    """
    Placeholder function for documentation of the API
    """
    contracts = Contract.query.all()
    data = ContractSchema(many=True).dump(contracts)
    return render_template("display_contracts.html", contracts=data)


@app.route("/dataview/users")
def display_users():
    """
    Placeholder function for documentation of the API
    """
    users = User.query.all()
    data = UserSchema(many=True).dump(users)
    print(data)
    return render_template("display_users.html", users=data)
