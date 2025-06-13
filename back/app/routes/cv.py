from flask import request
from flask_restful import Resource


class CVAPI(Resource):
    def get(self):
        return {"cv": {"name": "User Name"}}, 200

    def post(self):
        return {"message": "CV generated"}, 201

    def put(self):
        data = request.get_json()
        return {"message": "CV updated", "data": data}, 200
