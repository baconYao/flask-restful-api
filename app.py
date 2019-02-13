# Systems
from pathlib import Path
from os import system
# 3rd Party
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
# Ours
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# 檢查是否有data.db檔案
# db_file = Path("data.db")
# if not db_file.exists():
#     system("python create_table.py")
# else:
#     system("rm data.db")
#     system("python create_table.py")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'asasdasf'
api = Api(app)

# 自動建立data.db (定義在22行)
@app.before_first_request           # 在第一個request進來之前
def create_tables():
    db.create_all()

jtw = JWT(app, authenticate, identity)      # POST /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
