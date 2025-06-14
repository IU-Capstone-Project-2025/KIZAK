from flask_restful import Resource


class HomepageAPI(Resource):
    def get(self):
        return {"message": "This is home page"}
