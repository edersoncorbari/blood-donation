#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps

from scraping import BloodScraping

app = Flask(__name__)
api = Api(app)


class BloodCurrentPosition(Resource):

    def get(self):
        return BloodScraping().getPosition()


api.add_resource(BloodCurrentPosition, '/blood-current-position')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
