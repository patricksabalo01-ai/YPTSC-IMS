from flask import Blueprint, render_template
from app.decorators import login_required
transactions_bp = Blueprint("transactions", __name__)
@transactions_bp.route("/transactions/purchase")
@login_required
def purchase():
    transaction_data = {"title": "Purchase Management", "module": "purchase"}
    return render_template(
        "transactions/purchase.html", transaction_data=transaction_data
    )
@transactions_bp.route("/transactions")
@login_required
def transactions():
    transaction_data = {"title": "Stock Transactions", "module": "transactions"}
    return render_template(
        "transactions/stock_transactions.html", transaction_data=transaction_data
    )
@transactions_bp.route("/transactions/delivery")
@login_required
def delivery():
    transaction_data = {"title": "Delivery Management", "module": "delivery"}
    return render_template(
        "transactions/delivery.html", transaction_data=transaction_data
    )
@transactions_bp.route("/transactions/repair")
@login_required
def repair_center():
    transaction_data = {"title": "Repair Center", "module": "repair"}
    return render_template(
        "transactions/repair_center.html", transaction_data=transaction_data
    )
@transactions_bp.route("/transactions/contracts")
@login_required
def contracts():
    transaction_data = {"title": "Contract Management", "module": "contracts"}
    return render_template(
        "transactions/contracts.html", transaction_data=transaction_data
    )
