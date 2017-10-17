from flask import Blueprint, request, make_response, jsonify
from enquiry.connect import *
from enquiry.queries_db import *
from enquiry.secondary import *

# create new blueprint
users_blueprint = Blueprint('users', 'users', url_prefix='/user')


@users_blueprint.route('/<nickname>/create', methods=['POST'])
def create_user(nickname):
    content = request.get_json(silent=True)
    about = content['about']
    email = content['email']
    fullname = content['fullname']
    is_user_exist = False

    connect = connectDB()
    cursor = connect.cursor()

    try:
        cursor = queries(cursor, INSERT_USER, [nickname, about, email, fullname, ])
        connect.commit()
    except:
        is_user_exist = True

    if is_user_exist:
        users = []
        param_name_array = ["nickname", "about", "email", "fullname"]
        cursor = queries(cursor, SELECT_USERS_BY_NICKNAME_OR_EMAIL, [nickname, email, ])

        for user in cursor.fetchall():
            users.append(dict(zip(param_name_array, user[1:])))

        return make_response(jsonify(users), 409)
    else:
        cursor.close()
        param_name_array = ["nickname", "about", "email", "fullname"]
        param_value_array = [nickname, about, email, fullname]
        user = dict(zip(param_name_array, param_value_array))

        return make_response(jsonify(user), 201)


@users_blueprint.route('/<nickname>/profile', methods=['GET'])
def get_user_profile(nickname):
    connect = connectDB()
    cursor = connect.cursor()

    cursor = queries(cursor, SELECT_USERS_BY_NICKNAME, [nickname, ])

    if cursor.rowcount == 0:
        cursor.close()

        return make_response(jsonify({"message": "Can't find user with nickname = %s" % nickname}), 404)
    param_name_array = ["nickname", "about", "email", "fullname"]
    profile = dict(zip(param_name_array, cursor.fetchone()[1:]))
    cursor.close()

    return make_response(jsonify(profile), 200)


@users_blueprint.route('/<nickname>/profile', methods=['POST'] )
def change_user_profile(nickname):
    content = request.get_json(silent=True)
    is_not_empty = False
    about = ''
    email = ''
    fullname = ''

    connect = connectDB()
    cursor = connect.cursor()

    cursor = queries(cursor, SELECT_USERS_BY_NICKNAME, [nickname, ])

    if cursor.rowcount == 0:
        cursor.close()

        return make_response(jsonify({"message": "Can't find user with nickname = %s" % nickname}), 404)

    user = cursor.fetchone()
    param_array = ["nickname", "about", "email", "fullname"]
    user = dict(zip(param_array, user[1:]))

    if content is not None:
        if 'about' in content:
            about = content['about']
            is_not_empty = True
        else:
            about = user['about']

        if 'email' in content:
            email = content['email']
            is_not_empty = True
        else:
            email = user['email']

        if 'fullname' in content:
            fullname = content['fullname']
            is_not_empty = True
        else:
            fullname = user['fullname']

    if is_not_empty:
        try:
            cursor.execute(UPDATE_USER_BY_NICKNAME, [about, email, fullname, nickname, ])
        except:
            cursor.close()

            return make_response(jsonify({"message": "New user's data have conflict with existing"}), 409)
    param_name_array = ["nickname", "about", "email", "fullname"]
    # param_value_array = [nickname, about, email, fullname]
    # profile = dict(zip(param_name_array, param_value_array))
    cursor.execute(SELECT_USERS_BY_NICKNAME, [nickname, ])
    profile = dict(zip(param_name_array, cursor.fetchone()[1:]))
    cursor.close()

    return make_response(jsonify(profile), 200)
