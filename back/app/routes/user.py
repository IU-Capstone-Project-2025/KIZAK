from flask import request
from flask_restful import Resource


class UserAPI(Resource):
    def get(self, user_id):
        return {
            "id": user_id,
            "name": "User Name",
            "email": "user@mail.com",
        }, 200

    def post(self):
        return {"message": "User created"}, 201

    def delete(self, user_id):
        return {"message": f"User {user_id} deleted"}, 200

    def put(self, user_id):
        data = request.get_json()
        return {"message": f"User {user_id} updated", "data": data}, 200
