from flask import Flask, request
from flask_restx import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

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
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(debug=True)
