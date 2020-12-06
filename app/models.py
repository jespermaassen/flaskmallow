from sqlalchemy.sql.schema import Column
from app import db, ma
from app.enums import Ticker, ContractType
from marshmallow_enum import EnumField
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    contracts = db.relationship("Contract", backref="users", lazy="dynamic")

    def __str__(self):
        return f"<User {self.username}>"


class Contract(db.Model):
    __tablename__ = "contracts"
    id = db.Column(db.Integer, primary_key=True)
    contract_type = db.Column(db.Enum(ContractType))
    market = db.Column(db.Enum(Ticker))
    size = db.Column(db.Float(), nullable=False)
    entry_price = db.Column(db.Float(), nullable=False)
    date_open = db.Column(db.DateTime(), default=datetime.utcnow)
    date_close = db.Column(db.DateTime())
    status = db.Column(db.String(100), default="OPEN")
    trade_result = db.Column(db.Float(), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, user_id, contract_type, market, size, entry_price, date_close):
        self.user_id = user_id
        self.contract_type = contract_type
        self.market = market
        self.size = size
        self.entry_price = entry_price
        self.date_close = date_close

    def __str__(self):
        return (
            f"<Contract {self.id} | {self.market} | {self.size} | {self.entry_price} >"
        )


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class ContractSchema(ma.SQLAlchemyAutoSchema):
    # De-serialize Enums with Marshmallow
    market = EnumField(Ticker)
    contract_type = EnumField(ContractType)

    class Meta:
        model = Contract