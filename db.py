from api.controllers.users.views import users_blueprint
from flask import Flask

# from api.controllers.forums import forums_blueprint

app = Flask(__name__)

# app.register_blueprint(forums_blueprint)
app.register_blueprint(users_blueprint)

# @app.route('/')
# def hello_world():
#     conn = psycopg2.connect(host="localhost", database="students", user="postgres", password="lomogi99")
#     insert_command = "INSERT INTO students.public.forums VALUES (10, 'bananas', 105, 'bananas', 'same')"
#     select_command = "SELECT * FROM forums;"
#     cur = conn.cursor()
#     cur.execute(insert_command)
#     conn.commit()
#     cur.execute(select_command)
#     res = cur.fetchall()
#     cur.close()
#     conn.close()
#     print(res)
#     return 'Hello World!'


if __name__ == '__main__':
    app.run()
