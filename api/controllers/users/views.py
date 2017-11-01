from flask import Blueprint, request, make_response, jsonify
from api.services.UserService.UserService import UserService
from api.repositories.UserRepository.user_queries_db import *
from api.models.users.UserModel import UserModel
from api.repositories.connect import connectDB

# create new blueprint
users_blueprint = Blueprint('users', 'users', url_prefix='/api/user')

user_service = UserService()
user_model = UserModel
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
	connect = connectDB()
	cursor = connect.cursor()

	try:
		cursor.execute(INSERT_USER, [content['nickname'], content['about'], content['email'], content['fullname'], ])
		return make_response(jsonify(content), STATUS_CODE['CREATED'])
	except:
		users = []
		cursor.execute(SELECT_USERS_BY_NICKNAME_OR_EMAIL, [content['nickname'], content['email'], ])
		for user in cursor.fetchall():
			users.append(dict(zip(['nickname', 'about', 'email', 'fullname'], user[1:])))
		return make_response(jsonify(users), STATUS_CODE['CONFLICT'])


@users_blueprint.route('/<nickname>/profile', methods=['GET'])
def get_user_profile(nickname):
	connect = connectDB()
	cursor = connect.cursor()

	cursor.execute(SELECT_USERS_BY_NICKNAME, [nickname, ])
	user = cursor.fetchone()
	if user is None:
		return make_response(jsonify({"message": "Can't find user with nickname: " + nickname}), STATUS_CODE['NOT_FOUND'])

	content = dict()
	content['nickname'], content['about'], content['email'], content['fullname'] = user[1:]
	return make_response(jsonify(content), STATUS_CODE['OK'])


@users_blueprint.route('/<nickname>/profile', methods=['POST'])
def change_user_profile(nickname):
	content = request.get_json(silent=True)

	message_or_user, code = user_service.select_user_by_nickname(nickname)

	if code == STATUS_CODE['NOT_FOUND']:

		return make_response(jsonify(message_or_user), code)

	if code == STATUS_CODE['OK']:
		content['id'] = message_or_user.id
		new_user = user_model.from_dict(content)
		message_or_user.update_cls(new_user)

		message_or_user, code = user_service.update_user_by_nickname(message_or_user)

		if code == STATUS_CODE['OK']:
			param_name_array = ["nickname", "about", "email", "fullname"]
			param_value_array = [message_or_user.nickname, message_or_user.about, message_or_user.email,
								 message_or_user.fullname]
			message_or_user = dict(zip(param_name_array, param_value_array))

			return make_response(jsonify(message_or_user), code)

		if code == STATUS_CODE['CONFLICT']:

			return make_response(jsonify(message_or_user), code)
