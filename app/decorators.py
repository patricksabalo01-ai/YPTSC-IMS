from functools import wraps

from flask import (
    session,
    redirect,
    url_for,
    request,
    flash
)


# ==================================
# LOGIN REQUIRED
# ==================================

def login_required(function):

    @wraps(function)
    def wrapper(
        *args,
        **kwargs
    ):

        if "user_id" not in session:

            flash(
                "Please log in first.",
                "warning"
            )

            return redirect(

                url_for(
                    "auth.login",
                    next=request.url
                )

            )


        return function(
            *args,
            **kwargs
        )


    return wrapper

# ==================================
# ROLE REQUIRED
# ==================================

def role_required(
    *allowed_roles
):

    def decorator(
        function
    ):

        @wraps(function)
        def wrapper(
            *args,
            **kwargs
        ):

            if "user_id" not in session:

                flash(
                    "Please log in first.",
                    "warning"
                )

                return redirect(

                    url_for(
                        "auth.login"
                    )

                )


            current_role = session.get(
                "role"
            )


            if current_role not in allowed_roles:

                flash(
                    "You do not have permission to access this page.",
                    "danger"
                )

                return redirect(

                    url_for(
                        "dashboard.dashboard"
                    )

                )


            return function(
                *args,
                **kwargs
            )


        return wrapper


    return decorator