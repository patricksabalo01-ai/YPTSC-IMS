from flask import Flask, session, render_template

from flask_sqlalchemy import SQLAlchemy

from config import Config

# ==================================
# DATABASE
# ==================================

db = SQLAlchemy()


# ==================================
# APPLICATION FACTORY
# ==================================


def create_app():

    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    # ==================================
    # APPLICATION CONFIGURATION
    # ==================================

    app.config.from_object(Config)

    # ==================================
    # DATABASE INITIALIZATION
    # ==================================

    db.init_app(app)

    # ==================================
    # GLOBAL TEMPLATE VARIABLES
    # ==================================

    @app.context_processor
    def inject_global_data():

        return {
            "current_user": session.get("fullname"),
            "user_role": session.get("role"),
        }

    # ==================================
    # CACHE CONTROL
    # ==================================

    @app.after_request
    def add_cache_headers(response):

        response.headers["Cache-Control"] = (
            "no-store, " "no-cache, " "must-revalidate, " "max-age=0"
        )

        response.headers["Pragma"] = "no-cache"

        response.headers["Expires"] = "0"

        return response

    # ==================================
    # ERROR HANDLERS
    # ==================================

    @app.errorhandler(404)
    def not_found(error):

        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):

        return render_template("errors/500.html"), 500

    # ==================================
    # BLUEPRINT REGISTRATION
    # ==================================

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.inventory import inventory_bp
    from app.routes.transactions import transactions_bp
    from app.routes.reports import reports_bp
    from app.routes.admin import admin_bp
    from app.routes.deployment import deployment_bp

    app.register_blueprint(auth_bp)

    app.register_blueprint(dashboard_bp)

    app.register_blueprint(inventory_bp)

    app.register_blueprint(transactions_bp)

    app.register_blueprint(reports_bp)

    app.register_blueprint(admin_bp)
    
    app.register_blueprint(deployment_bp)

    return app
