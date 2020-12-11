from datetime import datetime
from app import app, db, ma, admin
from app.enums import ContractType, ContractStatus
from flask_admin.contrib.sqla import ModelView
from flask_user import UserManager, UserMixin, SQLAlchemyAdapter
from flask_user.passwords import hash_password
from marshmallow_enum import EnumField
from werkzeug.security import generate_password_hash


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default="")

    # User email information
    email = db.Column(db.String(255), nullable=True, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column("is_active", db.Boolean(), nullable=False, server_default="1")
    first_name = db.Column(db.String(100), nullable=False, server_default="")
    last_name = db.Column(db.String(100), nullable=False, server_default="")

    # Starting funds
    money = db.Column(db.Float(), default=100.0)

    # Relationships
    roles = db.relationship(
        "Role", secondary="user_roles", backref=db.backref("users", lazy="dynamic")
    )

    contracts = db.relationship("Contract", backref="users", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))


class Contract(db.Model):
    __tablename__ = "contracts"
    id = db.Column(db.Integer, primary_key=True)
    contract_type = db.Column(db.Enum(ContractType))
    market = db.Column(db.String(10), db.ForeignKey("assets.ticker"))
    size = db.Column(db.Float(), nullable=False)
    entry_price = db.Column(db.Float(), nullable=False)
    close_price = db.Column(db.Float(), nullable=True)
    date_open = db.Column(db.DateTime(), default=datetime.utcnow)
    date_close = db.Column(db.DateTime())
    status = db.Column(db.Enum(ContractStatus), default=ContractStatus["open"].value)
    trade_result_usd = db.Column(db.Float(), nullable=True)
    trade_result_pct = db.Column(db.Float(), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __str__(self):
        return (
            f"<Contract {self.id} | {self.market} | {self.size} | {self.entry_price} >"
        )


class Asset(db.Model):
    __tablename__ = "assets"
    ticker = db.Column(db.String(10), primary_key=True)
    asset_1 = db.Column(db.String(255))
    asset_2 = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class ContractSchema(ma.SQLAlchemyAutoSchema):
    # De-serialize Enums with Marshmallow
    contract_type = EnumField(ContractType)

    class Meta:
        model = Contract
        include_fk = True


class UserView(ModelView):
    column_display_pk = True
    inline_models = [Contract]

    def _on_model_change(self, form, model, is_created):
        model.password = hash_password(user_manager, model.password)


# Add views to admin panel
admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(Contract, db.session))

# Init User management features in admin panel
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)