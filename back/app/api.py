from flask_restful import Api
from .routes.user import UserAPI
from .routes.roadmap import RoadmapAPI
from .routes.cv import CVAPI


def init_routes(app):
    api = Api(app)

    api.add_resource(UserAPI, "/user", "/user/<int:user_id>")
    api.add_resource(RoadmapAPI, "/roadmap")
    api.add_resource(CVAPI, "/cv")
