from app import app, db
from app.models import *
from flask_user.passwords import hash_password

db.session.commit()
db.drop_all()
db.create_all()

# Bootstrap the database with data
# Assets
btc = Asset(ticker="btc_usd", asset_1="btc", asset_2="usd")
eth = Asset(ticker="eth_usd", asset_1="eth", asset_2="usd")
ltc = Asset(ticker="ltc_usd", asset_1="ltc", asset_2="usd")
xrp = Asset(ticker="xrp_usd", asset_1="xrp", asset_2="usd")

# Roles
admin_role = Role(name="admin")
user_role = Role(name="user")

# Users
jesper = User(
    username="jmaassen",
    password=hash_password(user_manager, "secretpass"),
    email="jesper@realmail.com",
    first_name="Jesper",
    last_name="Maassen",
)

herman = User(
    username="herman",
    password=hash_password(user_manager, "verysecret"),
    email="herman@realmail.com",
    first_name="Herman",
    last_name="Jansen",
)

# Contracts
contract_01 = Contract(
    contract_type=ContractType["long"].value,
    market="btc_usd",
    size=10.0,
    entry_price=18200.00,
    user_id=1,
)

contract_02 = Contract(
    contract_type=ContractType["long"].value,
    market="eth_usd",
    size=10.0,
    entry_price=550.00,
    user_id=1,
)

contract_03 = Contract(
    contract_type=ContractType["long"].value,
    market="eth_usd",
    size=5.0,
    entry_price=550.50,
    user_id=2,
)


db.session.add(btc)
db.session.add(eth)
db.session.add(ltc)
db.session.add(xrp)
db.session.add(admin_role)
db.session.add(user_role)
db.session.add(jesper)
db.session.add(herman)
db.session.add(contract_01)
db.session.add(contract_02)
db.session.add(contract_03)


db.session.commit()
