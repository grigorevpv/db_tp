from flask import Blueprint, request, make_response, jsonify
from api.services.UserService.UserService import UserService
from api.repositories.UserRepository.user_queries_db import *
from api.models.users.UserModel import UserModel
from api.repositories.connect import PostgresDataContext
from classes.base_blueprint import BaseBlueprint

user_service = UserService()
user_model = UserModel
data_context = PostgresDataContext()
STATUS_CODE = {
    'OK': 200,
    'CREATED': 201,
    'NOT_FOUND': 404,
    'CONFLICT': 409
}


class UserBlueprint(BaseBlueprint):
    def __init__(self):
        super().__init__()
        self._name = 'users'

    def _create_blueprint(self):
        blueprint = Blueprint(self._name, __name__)

        @blueprint.route('user/<nickname>/create', methods=['POST'])
        def create_user(nickname):
            content = request.get_json(silent=True)
            content['nickname'] = nickname
            connect, cursor = data_context.create_connection()

            try:
                cursor.execute(INSERT_USER,
                               [content['nickname'], content['about'], content['email'], content['fullname'], ])
                data_context.put_connection(connect)
                cursor.close()
                return make_response(jsonify(content), STATUS_CODE['CREATED'])
            except:
                users = []
                cursor.execute(SELECT_USERS_BY_NICKNAME_OR_EMAIL, [content['nickname'], content['email'], ])
                data = cursor.fetchall()
                data_context.put_connection(connect)
                cursor.close()
                return make_response(jsonify(data), STATUS_CODE['CONFLICT'])

        return blueprint


# # create new blueprint
# users_blueprint = Blueprint('users', 'users', url_prefix='/api/user')
#
# user_service = UserService()
# user_model = UserModel
# data_context = PostgresDataContext()
# STATUS_CODE = {
#     'OK': 200,
#     'CREATED': 201,
#     'NOT_FOUND': 404,
#     'CONFLICT': 409
# }
#
#
# @users_blueprint.route('/<nickname>/create', methods=['POST'])
# def create_user(nickname):
#     content = request.get_json(silent=True)
#     content['nickname'] = nickname
#     connect, cursor = data_context.create_connection()
#
#     try:
#         cursor.execute(INSERT_USER, [content['nickname'], content['about'], content['email'], content['fullname'], ])
#         data_context.put_connection(connect)
#         cursor.close()
#         return make_response(jsonify(content), STATUS_CODE['CREATED'])
#     except:
#         users = []
#         cursor.execute(SELECT_USERS_BY_NICKNAME_OR_EMAIL, [content['nickname'], content['email'], ])
#         data = cursor.fetchall()
#         data_context.put_connection(connect)
#         cursor.close()
#         return make_response(jsonify(data), STATUS_CODE['CONFLICT'])
#
#
# @users_blueprint.route('/<nickname>/profile', methods=['GET'])
# def get_user_profile(nickname):
#     connect, cursor = data_context.create_connection()
#
#     cursor.execute(SELECT_USERS_BY_NICKNAME, [nickname, ])
#     user = cursor.fetchone()
#     if user is None:
#         data_context.put_connection(connect)
#         cursor.close()
#         return make_response(jsonify({"message": "Can't find user with nickname: " + nickname}), STATUS_CODE['NOT_FOUND'])
#
#     data_context.put_connection(connect)
#     cursor.close()
#     return make_response(jsonify(user), STATUS_CODE['OK'])
#
#
# @users_blueprint.route('/<nickname>/profile', methods=['POST'])
# def change_user_profile(nickname):
#     connect, cursor = data_context.create_connection()
#
#     cursor.execute(SELECT_USERS_BY_NICKNAME, [nickname, ])
#     user = cursor.fetchone()
#     if user is None:
#         data_context.put_connection(connect)
#         cursor.close()
#         return make_response(jsonify({"message": "Can't find user with nickname: " + nickname}),
#                              STATUS_CODE['NOT_FOUND'])
#
#     content = request.get_json(silent=True)
#
#     if 'nickname' not in content:
#         content['nickname'] = user['nickname']
#
#     if 'about' not in content:
#         content['about'] = user['about']
#
#     if 'email' not in content:
#         content['email'] = user['email']
#
#     if 'fullname' not in content:
#         content['fullname'] = user['fullname']
#
#     try:
#         cursor.execute(UPDATE_USER_BY_NICKNAME, [content['about'], content['email'], content['fullname'], content['nickname'], ])
#         updated_user = cursor.fetchone()
#         data_context.put_connection(connect)
#         cursor.close()
#         return make_response(jsonify(updated_user), STATUS_CODE['OK'])
#     except:
#         data_context.put_connection(connect)
#         cursor.close()
#         return make_response(jsonify(content), STATUS_CODE['CONFLICT'])
#
#

