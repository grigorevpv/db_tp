from flask import Blueprint, request, make_response, jsonify
from api.services.UserService.UserService import UserService
from api.repositories.UserRepository.user_queries_db import *
from api.models.users.UserModel import UserModel
from api.repositories.connect import connectDB, PostgresDataContext

# create new blueprint
users_blueprint = Blueprint('users', 'users', url_prefix='/api/user')

user_service = UserService()
user_model = UserModel
data_context = PostgresDataContext()
STATUS_CODE = {
    'OK': 200,
    'CREATED': 201,
    'NOT_FOUND': 404,
    'CONFLICT': 409
}


@users_blueprint.route('/<nickname>/create', methods=['POST'])
def create_user(nickname):
    content = request.get_json(silent=True)
    content['nickname'] = nickname
    connect, cursor = data_context.create_connection()

    try:
        cursor.execute(INSERT_USER, [content['nickname'], content['about'], content['email'], content['fullname'], ])
        data_context.put_connection(connect)
        cursor.close()
        return make_response(jsonify(content), STATUS_CODE['CREATED'])
    except:
        users = []
        cursor.execute(SELECT_USERS_BY_NICKNAME_OR_EMAIL, [content['nickname'], content['email'], ])
        data = cursor.fetchall()
        # for user in cursor.fetchall():
        #     users.append(dict(zip(['nickname', 'about', 'email', 'fullname'], user[1:])))
        data_context.put_connection(connect)
        cursor.close()
        return make_response(jsonify(data), STATUS_CODE['CONFLICT'])


@users_blueprint.route('/<nickname>/profile', methods=['GET'])
def get_user_profile(nickname):
    connect, cursor = data_context.create_connection()

    cursor.execute(SELECT_USERS_BY_NICKNAME, [nickname, ])
    user = cursor.fetchone()
    if user is None:
        data_context.put_connection(connect)
        cursor.close()
        return make_response(jsonify({"message": "Can't find user with nickname: " + nickname}), STATUS_CODE['NOT_FOUND'])

    # content = dict()
    # content['nickname'], content['about'], content['email'], content['fullname'] = user[1:]
    data_context.put_connection(connect)
    cursor.close()
    return make_response(jsonify(user), STATUS_CODE['OK'])


@users_blueprint.route('/<nickname>/profile', methods=['POST'])
def change_user_profile(nickname):
    content = request.get_json(silent=True)
    connect = connectDB()
    cursor = connect.cursor()

    cursor.execute(SELECT_USERS_BY_NICKNAME, [nickname, ])
    user = cursor.fetchone()
    if user is None:
        cursor.close()
        return make_response(jsonify({"message": "Can't find user with nickname: " + nickname}),
                             STATUS_CODE['NOT_FOUND'])

    if 'nickname' not in content:
        content['nickname'] = user[1]

    if 'about' not in content:
        content['about'] = user[2]

    if 'email' not in content:
        content['email'] = user[3]

    if 'fullname' not in content:
        content['fullname'] = user[4]

    try:
        cursor.execute(UPDATE_USER_BY_NICKNAME, [content['about'], content['email'], content['fullname'], content['nickname'], ])
        updated_user = cursor.fetchone()
        content['nickname'], content['about'], content['email'], content['fullname'] = updated_user[1:]
        cursor.close()
        return make_response(jsonify(content), STATUS_CODE['OK'])
    except:
        cursor.close()
        return make_response(jsonify(content), STATUS_CODE['CONFLICT'])



