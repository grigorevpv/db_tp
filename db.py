from api.controllers.users.views import UserBlueprint, users_blueprint
from api.controllers.forums.views import forums_blueprint
from api.controllers.threads.views import threads_blueprint
from api.controllers.posts.views import posts_blueprint
from api.controllers.service.views import service_blueprint
from statement import Statement
from flask import Flask

# from api.controllers.forums import forums_blueprint

app = Flask(__name__)
# statement = Statement().register(app)

users_blp = UserBlueprint()
forum_blp = forums_blueprint
app.register_blueprint(forums_blueprint)
app.register_blueprint(users_blp.getBlueprint())
# app.register_blueprint(users_blueprint)
app.register_blueprint(threads_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(service_blueprint)

if __name__ == '__main__':
    app.run()
