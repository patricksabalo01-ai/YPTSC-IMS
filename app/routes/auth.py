from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash
)
from sqlalchemy import or_
from app.models import User
# AUTHENTICATION BLUEPRINT
auth_bp = Blueprint(
    "auth",
    __name__
)
# LOGIN
@auth_bp.route(
    "/login",
    methods=[
        "GET",
        "POST"
    ]
)
def login():
    # ALREADY LOGGED IN
    if "user_id" in session:
        return redirect(
            url_for(
                "dashboard.dashboard"
            )
        )
    # DISPLAY LOGIN PAGE
    if request.method == "GET":
        return render_template(
            "auth/login.html"
        )
    # GET LOGIN DATA
    login_input = (
        request.form.get(
            "login"
        )
        or ""
    ).strip()
    password = (
        request.form.get(
            "password"
        )
        or ""
    )
    # VALIDATE INPUT
    if not login_input or not password:
        flash(
            "Please enter your username or email and password.",
            "danger"
        )
        return redirect(
            url_for(
                "auth.login"
            )
        )
    # FIND USER
    # USERNAME OR EMAIL
    user = User.query.filter(
        or_(
            User.username == login_input,
            User.email == login_input.lower()
        )
    ).first()
    # INVALID ACCOUNT
    if user is None:
        flash(
            "Invalid username, email, or password.",
            "danger"
        )
        return redirect(
            url_for(
                "auth.login"
            )
        )
    # CHECK ACCOUNT STATUS
    if not user.is_active:
        flash(
            "This account is inactive. Please contact the system administrator.",
            "danger"
        )
        return redirect(
            url_for(
                "auth.login"
            )
        )
    # VERIFY PASSWORD
    if not user.check_password(
        password
    ):
        flash(
            "Invalid username, email, or password.",
            "danger"
        )
        return redirect(
            url_for(
                "auth.login"
            )
        )
    # CREATE USER SESSION
    session.clear()
    session["user_id"] = user.id
    session["user"] = user.username
    session["fullname"] = user.full_name
    session["role"] = user.role
    # LOGIN SUCCESS
    flash(
        f"Welcome back, {user.full_name}!",
        "success"
    )
    # ROLE-BASED REDIRECT
    if user.role == "Client":
        return redirect(
            url_for(
                "dashboard.dashboard"
            )
        )
    return redirect(
        url_for(
            "dashboard.dashboard"
        )
    )
# LOGOUT
@auth_bp.route(
    "/logout"
)
def logout():
    full_name = session.get(
        "fullname",
        "User"
    )
    session.clear()
    flash(
        f"{full_name} has been logged out.",
        "success"
    )
    return redirect(
        url_for(
            "auth.login"
        )
    )
