from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app import db

from app.models import (
    UnitInventory,
    Deployment
)

from app.decorators import login_required


# ==================================
# DEPLOYMENT BLUEPRINT
# ==================================

deployment_bp = Blueprint(
    "deployment",
    __name__
)
# ==================================
# SEARCH AVAILABLE UNITS
# ==================================

@deployment_bp.route(
    "/deployment/search-units"
)
@login_required
def search_units():

    # ==================================
    # GET SEARCH VALUE
    # ==================================

    search = (

        request.args.get(
            "search",
            ""
        )

        .strip()

    )


    # ==================================
    # EMPTY SEARCH
    # ==================================

    if not search:

        return {

            "units": []

        }


    # ==================================
    # SEARCH AVAILABLE UNITS
    # ==================================

    units = (

        UnitInventory.query

        .filter(

            UnitInventory.status
            == "Available",

            db.or_(

                UnitInventory.asset_code
                .ilike(
                    f"%{search}%"
                ),

                UnitInventory.brand
                .ilike(
                    f"%{search}%"
                ),

                UnitInventory.model
                .ilike(
                    f"%{search}%"
                ),

                UnitInventory.serial_number
                .ilike(
                    f"%{search}%"
                )

            )

        )

        .order_by(

            UnitInventory.asset_code.asc()

        )

        .limit(
            10
        )

        .all()

    )


    # ==================================
    # RETURN JSON
    # ==================================

    return {

        "units": [

            {

                "id":
                    unit.id,

                "asset_code":
                    unit.asset_code,

                "unit_category":
                    unit.unit_category,

                "brand":
                    unit.brand,

                "model":
                    unit.model,

                "serial_number":
                    unit.serial_number,

                "status":
                    unit.status

            }

            for unit in units

        ]

    }

# ==================================
# DEPLOYMENT PAGE
# ==================================

@deployment_bp.route(
    "/deployment",
    methods=[
        "GET",
        "POST"
    ]
)
@login_required
def deployment():


    # ==================================
    # GET AVAILABLE UNITS
    # ==================================

    available_units = (

        UnitInventory.query

        .filter_by(
            status="Available"
        )

        .order_by(
            UnitInventory.asset_code.asc()
        )

        .all()

    )


    # ==================================
    # DISPLAY DEPLOYMENT PAGE
    # ==================================

    if request.method == "GET":

        return render_template(

            "deployment/deployment.html",

            available_units=available_units

        )


    # ==================================
    # GET FORM DATA
    # ==================================

    unit_id = (
        request.form.get(
            "unit_id"
        )
        or ""
    ).strip()


    company_name = (
        request.form.get(
            "company_name"
        )
        or ""
    ).strip()


    sales_agent = (
        request.form.get(
            "sales_agent"
        )
        or ""
    ).strip()


    contract_start = (
        request.form.get(
            "contract_start"
        )
        or ""
    ).strip()


    contract_end = (
        request.form.get(
            "contract_end"
        )
        or ""
    ).strip()


    monthly_rate = (
        request.form.get(
            "monthly_rate"
        )
        or ""
    ).strip()


    department = (
        request.form.get(
            "department"
        )
        or ""
    ).strip()


    location = (
        request.form.get(
            "location"
        )
        or ""
    ).strip()


    deployment_date = (
        request.form.get(
            "deployment_date"
        )
        or ""
    ).strip()


    transaction_type = (
        request.form.get(
            "transaction_type"
        )
        or ""
    ).strip()


    technician = (
        request.form.get(
            "technician"
        )
        or ""
    ).strip()


    black_meter = (
        request.form.get(
            "black_meter"
        )
        or "0"
    ).strip()


    color_meter = (
        request.form.get(
            "color_meter"
        )
        or "0"
    ).strip()


    remarks = (
        request.form.get(
            "remarks"
        )
        or ""
    ).strip()


    # ==================================
    # REQUIRED FIELD VALIDATION
    # ==================================

    if not unit_id:

        flash(

            "Please select an available unit.",

            "danger"

        )

        return redirect(

            url_for(
                "deployment.deployment"
            )

        )


    if not company_name:

        flash(

            "Company name is required.",

            "danger"

        )

        return redirect(

            url_for(
                "deployment.deployment"
            )

        )


    # ==================================
    # CONVERT UNIT ID
    # ==================================

    try:

        unit_id = int(
            unit_id
        )

    except ValueError:

        flash(

            "Invalid unit selected.",

            "danger"

        )

        return redirect(

            url_for(
                "deployment.deployment"
            )

        )


    # ==================================
    # GET SELECTED UNIT
    # ==================================

    selected_unit = (

        UnitInventory.query

        .filter_by(
            id=unit_id
        )

        .first()

    )


    # ==================================
    # CHECK UNIT
    # ==================================

    if selected_unit is None:

        flash(

            "The selected unit was not found.",

            "danger"

        )

        return redirect(

            url_for(
                "deployment.deployment"
            )

        )


    # ==================================
    # CHECK UNIT AVAILABILITY
    # ==================================

    if selected_unit.status != "Available":

        flash(

            "This unit is no longer available.",

            "danger"

        )

        return redirect(

            url_for(
                "deployment.deployment"
            )

        )


    # ==================================
    # CONVERT DATE VALUES
    # ==================================

    try:

        contract_start_value = (

            datetime.strptime(

                contract_start,

                "%Y-%m-%d"

            ).date()

            if contract_start

            else None

        )


        contract_end_value = (

            datetime.strptime(

                contract_end,

                "%Y-%m-%d"

            ).date()

            if contract_end

            else None

        )


        deployment_date_value = (

            datetime.strptime(

                deployment_date,

                "%Y-%m-%d"

            ).date()

            if deployment_date

            else None

        )


    except ValueError:

        flash(

            "One or more dates are invalid.",

            "danger"

        )

        return redirect(

            url_for(
                "deployment.deployment"
            )

        )


    # ==================================
    # CONVERT NUMBER VALUES
    # ==================================

    try:

        monthly_rate_value = (

            float(
                monthly_rate
            )

            if monthly_rate

            else None

        )


        black_meter_value = int(

            black_meter

        )


        color_meter_value = int(

            color_meter

        )


    except ValueError:

        flash(

            "Monthly rate and meter values must be valid numbers.",

            "danger"

        )

        return redirect(

            url_for(
                "deployment.deployment"
            )

        )


    # ==================================
    # CREATE DEPLOYMENT
    # ==================================

    try:

        new_deployment = Deployment(

            unit_id=unit_id,

            company_name=company_name,

            sales_agent=(
                sales_agent
                or None
            ),

            contract_start=(
                contract_start_value
            ),

            contract_end=(
                contract_end_value
            ),

            monthly_rate=(
                monthly_rate_value
            ),

            department=(
                department
                or None
            ),

            location=(
                location
                or None
            ),

            deployment_date=(
                deployment_date_value
            ),

            transaction_type=(
                transaction_type
                or None
            ),

            technician=(
                technician
                or None
            ),

            black_meter=(
                black_meter_value
            ),

            color_meter=(
                color_meter_value
            ),

            remarks=(
                remarks
                or None
            )

        )


        # ==================================
        # SAVE DEPLOYMENT
        # ==================================

        db.session.add(

            new_deployment

        )


        # ==================================
        # UPDATE UNIT STATUS
        # ==================================

        selected_unit.status = (

            "Installed"

        )


        # ==================================
        # COMMIT DATABASE
        # ==================================

        db.session.commit()


        # ==================================
        # SUCCESS MESSAGE
        # ==================================

        flash(

            "Unit deployed successfully.",

            "success"

        )


        return redirect(

            url_for(
                "deployment.deployment"
            )

        )


    # ==================================
    # DATABASE ERROR
    # ==================================

    except Exception as error:

        db.session.rollback()


        flash(

            f"Unable to save deployment: {error}",

            "danger"

        )


        return redirect(

            url_for(
                "deployment.deployment"
            )

        )