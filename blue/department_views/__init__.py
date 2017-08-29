from flask import Blueprint

department_views = Blueprint('department_views', __name__)

from . import views
