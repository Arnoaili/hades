from flask import Flask
from .project_views import project_views

from .department_views import department_views

app = Flask(__name__)
app.jinja_env.add_extension("chartkick.ext.charts")
app.secret_key = 'PS#yio`%_!((f_or(%)))s'

app.register_blueprint(project_views)

app.register_blueprint(department_views)
