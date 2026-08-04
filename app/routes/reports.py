from flask import Blueprint, render_template
from app.decorators import login_required

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports")
@login_required
def reports():
    reports_data = {
        "title": "Reports & Analytics",
        "module": "reports",
        "available_reports": [
            "Inventory Report",
            "Stock Movement Report",
            "Purchase Report",
            "Repair Report",
        ],
    }
    return render_template("reports/reports.html", reports_data=reports_data)
