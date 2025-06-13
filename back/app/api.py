from flask_restful import Api

from .routes.cv import CVAPI
from .routes.roadmap import RoadmapAPI
from .routes.user import UserAPI


def init_routes(app):
    api = Api(app)

    api.add_resource(UserAPI, "/user", "/user/<int:user_id>")
    api.add_resource(RoadmapAPI, "/it roadmap")
    api.add_resource(CVAPI, "/cv")
