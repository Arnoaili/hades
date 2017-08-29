from flask import Blueprint
#from flask_restful import Api, Resource

project_views = Blueprint('project_views', __name__)
#api = Api(blue)


from . import views
