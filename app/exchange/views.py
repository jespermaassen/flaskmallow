from app import app
from app.models import *
from app.enums import *
from flask import request, jsonify, render_template


@app.route("/")
def exchange_home():
    """
    Placeholder function for documentation of the API
    """
    return render_template("base.html")
