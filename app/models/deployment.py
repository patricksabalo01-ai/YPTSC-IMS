from app import db


# ==================================
# DEPLOYMENT MODEL
# ==================================

class Deployment(db.Model):

    __tablename__ = "deployments"


    # ==================================
    # PRIMARY KEY
    # ==================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # ==================================
    # UNIT RELATION
    # ==================================

    unit_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "units_inv.id",
            ondelete="RESTRICT"
        ),
        nullable=False
    )


    # ==================================
    # CLIENT INFORMATION
    # ==================================

    company_name = db.Column(
        db.String(150),
        nullable=False
    )


    sales_agent = db.Column(
        db.String(150),
        nullable=True
    )


    # ==================================
    # CONTRACT INFORMATION
    # ==================================

    contract_start = db.Column(
        db.Date,
        nullable=True
    )


    contract_end = db.Column(
        db.Date,
        nullable=True
    )


    monthly_rate = db.Column(
        db.Numeric(
            12,
            2
        ),
        nullable=True
    )


    # ==================================
    # DEPLOYMENT INFORMATION
    # ==================================

    department = db.Column(
        db.String(150),
        nullable=True
    )


    location = db.Column(
        db.String(150),
        nullable=True
    )


    deployment_date = db.Column(
        db.Date,
        nullable=True
    )


    transaction_type = db.Column(
        db.String(100),
        nullable=True
    )


    technician = db.Column(
        db.String(150),
        nullable=True
    )


    # ==================================
    # METER READINGS
    # ==================================

    black_meter = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )


    color_meter = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )


    # ==================================
    # REMARKS
    # ==================================

    remarks = db.Column(
        db.Text,
        nullable=True
    )


    # ==================================
    # DATE CREATED
    # ==================================

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )


    # ==================================
    # UNIT RELATIONSHIP
    # ==================================

    unit = db.relationship(
        "UnitInventory",
        backref=db.backref(
            "deployments",
            lazy=True
        )
    )