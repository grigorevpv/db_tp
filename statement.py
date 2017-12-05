from api.controllers.users.views import UserBlueprint
from injector import inject, singleton


class Statement(object):

    def register(self, app):
        app.register_blueprint(UserBlueprint(), url_prefix='/')
