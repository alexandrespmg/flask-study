from flask import Flask, request
from flask_restx import Resource, Api
from flask_jwt import JWT, jwt_required

from security import identity, authenticate

app = Flask(__name__)
app.secret_key = 'example-of-secret-key'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):
    def get(self, name):
        item = self.get_item(name)

        return {'item': item}, 200 if item else 404

    def get_item(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return item

    def post(self, name):
        if self.get_item(name):
            return {'message': 'An item with name {} already exists'.format(name)}, 422
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return {'item': item}, 201


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(debug=True)
