from flask import Blueprint, request, make_response, jsonify
from api.services.UserService.UserService import UserService
from api.models.users.UserModel import UserModel

# create new blueprint
users_blueprint = Blueprint('users', 'users', url_prefix='/user')

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
    user = user_model.from_dict(content)

    user, code = user_service.create_user(user)

    if code == STATUS_CODE['CREATED']:
        param_name_array = ["nickname", "about", "email", "fullname"]
        param_value_array = [user.nickname, user.about, user.email, user.fullname]
        user = dict(zip(param_name_array, param_value_array))

        return make_response(jsonify(user), code)

    if code == STATUS_CODE['CONFLICT']:

        return make_response(jsonify(user), code)


@users_blueprint.route('/<nickname>/profile', methods=['GET'])
def get_user_profile(nickname):
    content = dict()
    content['nickname'] = nickname
    user = user_model.from_dict(content)

    message_or_user, code = user_service.select_user_by_nickname(user)

    if code == STATUS_CODE['OK']:
        param_name_array = ["nickname", "about", "email", "fullname"]
        param_value_array = [message_or_user.nickname, message_or_user.about, message_or_user.email, message_or_user.fullname]
        message_or_user = dict(zip(param_name_array, param_value_array))

        return make_response(jsonify(message_or_user), code)

    if code == STATUS_CODE['NOT_FOUND']:

        return make_response(jsonify(message_or_user), code)


@users_blueprint.route('/<nickname>/profile', methods=['POST'])
def change_user_profile(nickname):
    content = request.get_json(silent=True)
    content['nickname'] = nickname
    user = user_model.from_dict(content)

    message_or_user, code = user_service.select_user_by_nickname(user)

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





# @users_blueprint.route('/<nickname>/profile', methods=['POST'] )
# def change_user_profile(nickname):
#     content = request.get_json(silent=True)
#     is_not_empty = False
#     about = ''
#     email = ''
#     fullname = ''
#
#     connect = connectDB()
#     cursor = connect.cursor()
#
#     cursor = queries(cursor, SELECT_USERS_BY_NICKNAME, [nickname, ])
#
#     if cursor.rowcount == 0:
#         cursor.close()
#
#         return make_response(jsonify({"message": "Can't find user with nickname = %s" % nickname}), 404)
#
#     user = cursor.fetchone()
#     param_array = ["nickname", "about", "email", "fullname"]
#     user = dict(zip(param_array, user[1:]))
#
#     if content is not None:
#         if 'about' in content:
#             about = content['about']
#             is_not_empty = True
#         else:
#             about = user['about']
#
#         if 'email' in content:
#             email = content['email']
#             is_not_empty = True
#         else:
#             email = user['email']
#
#         if 'fullname' in content:
#             fullname = content['fullname']
#             is_not_empty = True
#         else:
#             fullname = user['fullname']
#
#     if is_not_empty:
#         try:
#             cursor.execute(UPDATE_USER_BY_NICKNAME, [about, email, fullname, nickname, ])
#         except:
#             cursor.close()
#
#             return make_response(jsonify({"message": "New user's data have conflict with existing"}), 409)
#     param_name_array = ["nickname", "about", "email", "fullname"]
#     # param_value_array = [nickname, about, email, fullname]
#     # profile = dict(zip(param_name_array, param_value_array))
#     cursor.execute(SELECT_USERS_BY_NICKNAME, [nickname, ])
#     profile = dict(zip(param_name_array, cursor.fetchone()[1:]))
#     cursor.close()
#
#     return make_response(jsonify(profile), 200)