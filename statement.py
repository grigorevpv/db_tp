from api.controllers.users.views import UserBlueprint

class Statement(object):
	def __init__(self):
		self._users_blueprint = UserBlueprint._create_blueprint()

	def register(self, app):
		app.register_blueprint(self._users_blueprint, url_prefix='/')
