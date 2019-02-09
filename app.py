# Systems
from pathlib import Path
from os import system
# 3rd Party
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
# Ours
from security import authenticate, identity
from user import UserRegister

# 檢查是否有data.db檔案
db_file = Path("data.db")
if not db_file.exists():
    system("python create_table.py")
else:
    system("rm data.db")
    system("python create_table.py")

app = Flask(__name__)
app.secret_key = 'asasdasf'
api = Api(app)

jtw = JWT(app, authenticate, identity)      # POST /auth

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )
    
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message':'An item with name {} already exists.'.format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201
    
    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}
    
    @jwt_required()
    def put(self, name):
        
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
