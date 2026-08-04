from sqlalchemy import func

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime

from app import db
from app.models import (
    UnitInventory,
    PartInventory,
)

from app.decorators import login_required
from app.utils.qr_generator import generate_qr

# ==================================================
# INVENTORY BLUEPRINT
# ==================================================

inventory_bp = Blueprint("inventory", __name__)


# ==================================================
# UNITS INVENTORY
# ==================================================


@inventory_bp.route("/inventory/units")
@login_required
def units_inventory():

    units = UnitInventory.query.order_by(UnitInventory.id.desc()).all()

    inventory_data = {"title": "Units Inventory", "module": "units", "units": units}

    return render_template(
        "inventory/units_inventory.html", inventory_data=inventory_data
    )


# ==================================================
# REGISTER UNIT PAGE
# ==================================================


@inventory_bp.route("/inventory/unit-register")
@login_required
def unit_register():

    register_data = {"title": "Register Unit", "module": "units"}

    return render_template("inventory/unit_register.html", register_data=register_data)


# ==================================================
# ASSET CODE GENERATOR
# ==================================================


def generate_asset_code():

    last_unit = UnitInventory.query.order_by(UnitInventory.id.desc()).first()

    if not last_unit:

        return "YPTSC-UNIT-00001"

    return f"YPTSC-UNIT-" f"{last_unit.id + 1:05d}"


# ==================================================
# REGISTER UNIT PROCESS
# ==================================================


@inventory_bp.route("/inventory/register-unit", methods=["POST"])
@login_required
def register_unit():

    serial_number = request.form.get("serial_number")

    existing_unit = UnitInventory.query.filter_by(serial_number=serial_number).first()

    if existing_unit:

        flash("Serial number already exists.", "danger")

        return redirect(url_for("inventory.unit_register"))

    asset_code = generate_asset_code()

    qr_code = generate_qr(asset_code)

    unit = UnitInventory(
        asset_code=asset_code,
        qr_code=qr_code,
        unit_category=request.form.get("unit_category"),
        brand=request.form.get("brand"),
        model=request.form.get("model"),
        serial_number=serial_number,
        ownership_type=request.form.get("ownership_type"),
        supplier=request.form.get("supplier"),
        purchase_date=request.form.get("purchase_date") or None,
        date_delivered=request.form.get("date_delivered") or None,
        purchase_price=request.form.get("purchase_price", type=float),
        warranty=request.form.get("warranty"),
        status=request.form.get("status"),
        
        # Creation and update timestamps
        created_at=datetime.utcnow(),
    )

    try:

        db.session.add(unit)

        db.session.commit()

        flash("Unit successfully registered.", "success")

    except Exception as error:

        db.session.rollback()

        flash(f"Database error: {error}", "danger")

        return redirect(url_for("inventory.unit_register"))

    return redirect(url_for("inventory.units_inventory"))


# ==================================================
# DELETE UNIT
# ==================================================


@inventory_bp.route("/inventory/delete-unit/<asset_code>", methods=["POST"])
@login_required
def delete_unit(asset_code):

    unit = UnitInventory.query.filter_by(asset_code=asset_code).first()

    if unit is None:

        flash("Unit not found.", "danger")

        return redirect(url_for("inventory.units_inventory"))

    try:

        db.session.delete(unit)

        db.session.commit()

        flash("Unit successfully deleted.", "success")

    except Exception as error:

        db.session.rollback()

        flash(f"Database error: {error}", "danger")

    return redirect(url_for("inventory.units_inventory"))


# ==================================================
# VIEW UNIT DETAILS
# ==================================================


@inventory_bp.route("/inventory/view-unit/<asset_code>")
@login_required
def view_unit(asset_code):

    unit = UnitInventory.query.filter_by(asset_code=asset_code).first()

    if unit is None:

        flash("Unit not found.", "danger")

        return redirect(url_for("inventory.units_inventory"))

    return render_template("inventory/unit_view.html", unit=unit)


# ==================================================
# EDIT UNIT PAGE
# ==================================================


@inventory_bp.route("/inventory/edit-unit/<asset_code>")
@login_required
def edit_unit(asset_code):

    unit = UnitInventory.query.filter_by(asset_code=asset_code).first()

    if unit is None:

        flash("Unit not found.", "danger")

        return redirect(url_for("inventory.units_inventory"))

    return render_template("inventory/unit_edit.html", unit=unit)


# ==================================================
# UPDATE UNIT
# ==================================================


@inventory_bp.route("/inventory/update-unit/<asset_code>", methods=["POST"])
@login_required
def update_unit(asset_code):
    unit = UnitInventory.query.filter_by(asset_code=asset_code).first()

    if unit is None:

        flash("Unit not found.", "danger")

        return redirect(url_for("inventory.units_inventory"))

    try:

        # ==================================
        # UNIT INFORMATION
        # ==================================

        unit.unit_category = request.form.get("unit_category")

        unit.brand = request.form.get("brand")

        unit.model = request.form.get("model")

        unit.serial_number = request.form.get("serial_number")

        # ==================================
        # OWNERSHIP / PURCHASE
        # ==================================

        unit.ownership_type = request.form.get("ownership_type")

        unit.supplier = request.form.get("supplier")

        unit.purchase_date = request.form.get("purchase_date") or None

        unit.date_delivered = request.form.get("date_delivered") or None

        unit.purchase_price = request.form.get("purchase_price") or None

        unit.warranty = request.form.get("warranty")

       
        

        unit.status = request.form.get("status")

        
        unit.updated_at = datetime.utcnow()

        # ==================================
        # SAVE CHANGES
        # ==================================

        db.session.commit()

        flash("Unit successfully updated.", "success")

    except Exception as error:

        db.session.rollback()

        flash(f"Unable to update unit: {error}", "danger")

    return redirect(url_for("inventory.units_inventory"))

    # ======================================
    # SERIAL DUPLICATE CHECK
    # ======================================

    for unit in units:

        if unit["serial_number"] == new_serial and unit["asset_code"] != asset_code:

            flash("Serial number already exists.", "danger")

            return redirect(url_for("inventory.edit_unit", asset_code=asset_code))

    # ======================================
    # UPDATE DATA
    # ======================================

    fields = [
        "unit_category",
        "brand",
        "model",
        "serial_number",
        "ownership_type",
        "supplier",
        "purchase_date",
        "date_delivered",
        "purchase_price",
        "warranty",
        "status",

    ]

    for field in fields:

        target_unit[field] = request.form.get(field)

    session["units_inventory"] = units

    flash("Unit successfully updated.", "success")

    return redirect(url_for("inventory.units_inventory"))


# ==================================================
# PARTS INVENTORY
# ==================================================


@inventory_bp.route(
    "/inventory/parts"
)
@login_required
def parts_inventory():

    parts = (

        PartInventory.query

        .order_by(
            PartInventory.id.desc()
        )

        .all()

    )


    inventory_data = {

        "title":
            "Parts Inventory",

        "module":
            "parts",

        "parts":
            parts,

    }


    return render_template(

        "inventory/parts_inventory.html",

        inventory_data=
        inventory_data,

    )


# ==================================================
# REGISTER PART PAGE
# ==================================================


@inventory_bp.route(
    "/inventory/part-register"
)
@login_required
def part_register():

    register_data = {

        "title":
            "Register Part",

        "module":
            "parts",

    }


    return render_template(

        "inventory/part_register.html",

        register_data=
        register_data,

    )


# ==================================================
# GENERATE PART CODE
# ==================================================


def generate_part_code():

    last_part = (

        PartInventory.query

        .order_by(
            PartInventory.id.desc()
        )

        .first()

    )


    if not last_part:

        return (
            "YPTSC-PART-00001"
        )


    return (

        f"YPTSC-PART-"

        f"{last_part.id + 1:05d}"

    )


# ==================================================
# AUTOMATIC STOCK STATUS
# ==================================================


def get_part_status(
    stock,
    minimum_stock
):

    if stock <= 0:

        return (
            "Out of Stock"
        )


    if (
        stock
        <=
        minimum_stock
    ):

        return (
            "Low Stock"
        )


    return (
        "Available"
    )


# ==================================================
# REGISTER PART PROCESS
# ==================================================


@inventory_bp.route(
    "/inventory/register-part",
    methods=["POST"]
)
@login_required
def register_part():

    part_number = (

        request.form.get(
            "part_number"
        )

        .strip()

    )


    existing_part = (

        PartInventory.query

        .filter_by(
            part_number=
            part_number
        )

        .first()

    )


    if existing_part:

        flash(

            "Part number already exists.",

            "danger"

        )


        return redirect(

            url_for(
                "inventory.part_register"
            )

        )


    stock = (

        request.form.get(
            "stock",
            type=int
        )

        or 0

    )


    minimum_stock = (

        request.form.get(
            "minimum_stock",
            type=int
        )

        or 0

    )


    part = PartInventory(

        part_code=
        generate_part_code(),

        category=
        request.form.get(
            "category"
        ),

        part_number=
        part_number,

        description=
        request.form.get(
            "description"
        ),

        brand=
        request.form.get(
            "brand"
        )
        or None,

        compatible_model=
        request.form.get(
            "compatible_model"
        )
        or None,

        supplier=
        request.form.get(
            "supplier"
        )
        or None,

        stock=
        stock,

        minimum_stock=
        minimum_stock,

        location=
        request.form.get(
            "location"
        )
        or None,

        # Automatically calculated
        # from stock quantity
        status=
        get_part_status(
            stock,
            minimum_stock
        ),

        remarks=
        request.form.get(
            "remarks"
        )
        or None,

        created_at=
        datetime.utcnow(),

    )


    try:

        db.session.add(
            part
        )


        db.session.commit()


        flash(

            "Part successfully registered.",

            "success"

        )


    except Exception as error:

        db.session.rollback()


        flash(

            f"Database error: {error}",

            "danger"

        )


        return redirect(

            url_for(
                "inventory.part_register"
            )

        )


    return redirect(

        url_for(
            "inventory.parts_inventory"
        )

    )


# ==================================================
# DELETE PART
# ==================================================


@inventory_bp.route(
    "/inventory/delete-part/<part_code>",
    methods=["POST"]
)
@login_required
def delete_part(
    part_code
):

    part = (

        PartInventory.query

        .filter_by(
            part_code=
            part_code
        )

        .first()

    )


    if part is None:

        flash(

            "Part not found.",

            "danger"

        )


        return redirect(

            url_for(
                "inventory.parts_inventory"
            )

        )


    try:

        db.session.delete(
            part
        )


        db.session.commit()


        flash(

            "Part successfully deleted.",

            "success"

        )


    except Exception as error:

        db.session.rollback()


        flash(

            f"Unable to delete part: {error}",

            "danger"

        )


    return redirect(

        url_for(
            "inventory.parts_inventory"
        )

    )


# ==================================================
# PRINT UNIT QR CODE
# ==================================================


@inventory_bp.route("/inventory/print-qr/<asset_code>")
@login_required
def print_qr(asset_code):

    units = session.get("units_inventory", [])

    unit = None

    for item in units:

        if item["asset_code"] == asset_code:

            unit = item

            break

    if not unit:

        flash("Unit not found.", "danger")

        return redirect(url_for("inventory.units_inventory"))

    return render_template("inventory/unit_qr_print.html", unit=unit)
