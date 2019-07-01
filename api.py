from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from parser import parse_building_address

app = Flask(__name__)
api = Api(app)


class Hello(Resource):
    def get(self):
        return 'This is address regex parser'

class parse(Resource):
    def get(self):
        qry = request.args.get('address')
        parsed = parse_building_address(qry)
        return parsed, 200


##
## Actually setup the Api resource routing here
##
api.add_resource(Hello, '/')
api.add_resource(parse, '/parse')


if __name__ == '__main__':
    app.run(debug=True)
