from app import db
class UnitInventory(db.Model):
    __tablename__ = "units_inv"
    # PRIMARY KEY
    id = db.Column(db.Integer, primary_key=True)
    # UNIT INFORMATION
    asset_code = db.Column(db.String(50), unique=True, nullable=False)
    qr_code = db.Column(db.String(255))
    unit_category = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    # OWNERSHIP / PURCHASE
    ownership_type = db.Column(db.String(100))
    supplier = db.Column(db.String(150))
    purchase_date = db.Column(db.Date)
    date_delivered = db.Column(db.Date)
    purchase_price = db.Column(db.Numeric(12, 2))
    warranty = db.Column(db.String(100))
    status = db.Column(db.String(50))
    # TIMESTAMPS
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
