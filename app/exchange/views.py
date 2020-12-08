from app import app
from app.models import *
from app.enums import *
from flask import render_template
from flask_user import login_required, roles_required, current_user


@app.route("/exchange")
@login_required
def exchange_home():
    """
    Returns homepage for the contract exchange
    """
    return render_template("exchange.html")