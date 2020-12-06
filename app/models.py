from app import db, ma, admin
from app.enums import Ticker, ContractType, ContractStatus
from marshmallow_enum import EnumField
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(50), unique=True)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    contracts = db.relationship("Contract", backref="users", lazy="dynamic")

    def __repr__(self):
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
    status = db.Column(db.Enum(ContractStatus), default=ContractStatus["open"].value)
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


from flask_admin.contrib.sqla import ModelView


class UserView(ModelView):
    column_display_pk = True

    def _on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password, method="sha256")


admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(Contract, db.session))