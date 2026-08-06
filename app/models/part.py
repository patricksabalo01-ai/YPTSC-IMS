from app import db
class PartInventory(
    db.Model
):
    __tablename__ = (
        "parts_inv"
    )
    # PRIMARY KEY
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    # PART INFORMATION
    part_code = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )
    category = db.Column(
        db.String(100),
        nullable=False
    )
    part_number = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )
    description = db.Column(
        db.String(255),
        nullable=False
    )
    brand = db.Column(
        db.String(100)
    )
    compatible_model = db.Column(
        db.String(200)
    )
    supplier = db.Column(
        db.String(150)
    )
    # STOCK
    stock = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )
    minimum_stock = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )
    location = db.Column(
        db.String(150)
    )
    status = db.Column(
        db.String(50),
        nullable=False
    )
    remarks = db.Column(
        db.Text
    )
    # TIMESTAMPS
    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now()
    )
