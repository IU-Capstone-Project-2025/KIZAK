from flask import request
from flask_restful import Resource


class RoadmapAPI(Resource):
    def get(self):
        return {
            "roadmap": [
                {"milestone": "Step 1", "completed": False},
                {"milestone": "Step 2", "completed": True},
            ]
        }, 200

    def put(self):
        data = request.get_json()
        return {"message": "Roadmap updated", "data": data}, 200
