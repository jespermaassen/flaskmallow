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


# Business logic.

# BASIC
# Interface for current pricing (charts)
# Users can open & close Contracts
# When the contract is closed, the trade result is updated in the contract table

# 2.0
# Allow user to set custom expiry dates, stop-loss en take-profits
