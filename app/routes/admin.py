from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db

from app.models import User

from app.decorators import (
    login_required,
    role_required
)

# ==================================
# ADMIN BLUEPRINT
# ==================================

admin_bp = Blueprint("admin", __name__)


# ==================================
# USER MANAGEMENT
# ==================================


@admin_bp.route("/admin/users")
@login_required
def users():

    # ==================================
    # GET ALL USERS FROM POSTGRESQL
    # ==================================

    users_list = User.query.order_by(User.created_at.desc()).all()

    # ==================================
    # PAGE DATA
    # ==================================

    users_data = {
        "title": "User Management",
        "module": "users",
        "roles": ["Admin", "Staff", "Technician", "Client"],
        "users": users_list,
    }

    return render_template("admin/users.html", users_data=users_data)


# ==================================
# REGISTER USER
# ==================================


@admin_bp.route("/admin/register-user", methods=["GET", "POST"])
@login_required
def register_user():

    # ==================================
    # DISPLAY REGISTER PAGE
    # ==================================

    if request.method == "GET":

        return render_template("admin/register_user.html")

    # ==================================
    # GET FORM DATA
    # ==================================

    full_name = (request.form.get("full_name") or "").strip()

    username = (request.form.get("username") or "").strip()

    email = (request.form.get("email") or "").strip().lower()

    password = request.form.get("password") or ""

    confirm_password = request.form.get("confirm_password") or ""

    role = request.form.get("role") or ""

    is_active = request.form.get("is_active") == "true"

    # ==================================
    # REQUIRED FIELD VALIDATION
    # ==================================

    if not all([full_name, username, email, password, confirm_password, role]):

        flash("Please complete all required fields.", "danger")

        return redirect(url_for("admin.register_user"))

    # ==================================
    # PASSWORD VALIDATION
    # ==================================

    if password != confirm_password:

        flash("Passwords do not match.", "danger")

        return redirect(url_for("admin.register_user"))

    if len(password) < 8:

        flash("Password must contain at least 8 characters.", "danger")

        return redirect(url_for("admin.register_user"))

    # ==================================
    # CHECK DUPLICATE USERNAME
    # ==================================

    existing_username = User.query.filter_by(username=username).first()

    if existing_username:

        flash("Username is already in use.", "danger")

        return redirect(url_for("admin.register_user"))

    # ==================================
    # CHECK DUPLICATE EMAIL
    # ==================================

    existing_email = User.query.filter_by(email=email).first()

    if existing_email:

        flash("Email address is already registered.", "danger")

        return redirect(url_for("admin.register_user"))

    # ==================================
    # CREATE USER
    # ==================================

    try:

        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
            role=role,
            is_active=is_active,
        )

        # ==================================
        # HASH PASSWORD
        # ==================================

        new_user.set_password(password)

        # ==================================
        # SAVE TO POSTGRESQL
        # ==================================

        db.session.add(new_user)

        db.session.commit()

        flash("User account created successfully.", "success")

        return redirect(url_for("admin.users"))

    except Exception as error:

        db.session.rollback()

        flash(f"Unable to create user: {error}", "danger")

        return redirect(url_for("admin.register_user"))


# ==================================
# UPDATE USER
# ==================================


@admin_bp.route("/admin/update-user/<int:user_id>", methods=["GET", "POST"])
@login_required
def update_user(user_id):

    # ==================================
    # GET USER
    # ==================================

    user = User.query.filter_by(id=user_id).first()

    # ==================================
    # USER NOT FOUND
    # ==================================

    if user is None:

        flash("User not found.", "danger")

        return redirect(url_for("admin.users"))

    # ==================================
    # DISPLAY UPDATE PAGE
    # ==================================

    if request.method == "GET":

        return render_template("admin/update_user.html", user=user)

    # ==================================
    # GET FORM DATA
    # ==================================

    full_name = (request.form.get("full_name") or "").strip()

    username = (request.form.get("username") or "").strip()

    email = (request.form.get("email") or "").strip().lower()

    role = request.form.get("role") or ""

    is_active = request.form.get("is_active") == "true"

    password = request.form.get("password") or ""

    confirm_password = request.form.get("confirm_password") or ""

    # ==================================
    # REQUIRED FIELD VALIDATION
    # ==================================

    if not all([full_name, username, email, role]):

        flash("Please complete all required fields.", "danger")

        return redirect(url_for("admin.update_user", user_id=user.id))

    # ==================================
    # CHECK DUPLICATE USERNAME
    # EXCLUDING CURRENT USER
    # ==================================

    existing_username = User.query.filter(
        User.username == username, User.id != user.id
    ).first()

    if existing_username:

        flash("Username is already used by another account.", "danger")

        return redirect(url_for("admin.update_user", user_id=user.id))

    # ==================================
    # CHECK DUPLICATE EMAIL
    # EXCLUDING CURRENT USER
    # ==================================

    existing_email = User.query.filter(User.email == email, User.id != user.id).first()

    if existing_email:

        flash("Email is already used by another account.", "danger")

        return redirect(url_for("admin.update_user", user_id=user.id))

    # ==================================
    # OPTIONAL PASSWORD VALIDATION
    # ==================================

    if password:

        if len(password) < 8:

            flash("New password must contain at least 8 characters.", "danger")

            return redirect(url_for("admin.update_user", user_id=user.id))

        if password != confirm_password:

            flash("New passwords do not match.", "danger")

            return redirect(url_for("admin.update_user", user_id=user.id))

    # ==================================
    # UPDATE USER
    # ==================================

    try:

        user.full_name = full_name

        user.username = username

        user.email = email

        user.role = role

        user.is_active = is_active

        # ==================================
        # UPDATE PASSWORD ONLY IF ENTERED
        # ==================================

        if password:

            user.set_password(password)

        # ==================================
        # SAVE CHANGES
        # ==================================

        db.session.commit()

        flash("User updated successfully.", "success")

        return redirect(url_for("admin.users"))

    except Exception as error:

        db.session.rollback()

        flash(f"Unable to update user: {error}", "danger")

        return redirect(url_for("admin.update_user", user_id=user.id))


# ==================================
# SYSTEM SETTINGS
# ==================================


@admin_bp.route("/admin/settings")
@login_required
def settings():

    settings_data = {
        "title": "System Settings",
        "module": "settings",
        "system_name": "YPTSC Inventory Management System",
    }

    return render_template("admin/settings.html", settings_data=settings_data)

# ==================================
# DELETE USER
# ==================================

@admin_bp.route(
    "/admin/delete-user/<int:user_id>",
    methods=["POST"]
)
@login_required
def delete_user(user_id):

    # ==================================
    # GET USER
    # ==================================

    user = User.query.filter_by(
        id=user_id
    ).first()


    # ==================================
    # USER NOT FOUND
    # ==================================

    if user is None:

        flash(
            "User not found.",
            "danger"
        )

        return redirect(
            url_for(
                "admin.users"
            )
        )


    # ==================================
    # DELETE USER
    # ==================================

    try:

        db.session.delete(
            user
        )

        db.session.commit()


        flash(
            "User deleted successfully.",
            "success"
        )


    except Exception as error:

        db.session.rollback()


        flash(
            f"Unable to delete user: {error}",
            "danger"
        )


    return redirect(
        url_for(
            "admin.users"
        )
    )