from blue import app
from flask.ext.script import Manager

# debug mode
if __name__ == '__main__':
    app.run(debug=True)

"""
#production mode
manager = Manager(app)

if __name__ == '__main__':
	manager.run()
"""