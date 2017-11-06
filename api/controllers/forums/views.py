from flask import Blueprint, request, make_response, jsonify
from api.services.ForumService.ForumService import ForumService
from api.models.forums.ForumModel import ForumModel
from api.services.UserService.UserService import UserService
from api.models.users.UserModel import UserModel
from api.services.ThreadService.ThreadServise import ThreadService
from api.models.threads.ThreadModel import ThreadModel
from api.repositories.connect import PostgresDataContext
from api.repositories.ForumRepository.forum_queries_db import *
from enquiry.queries_db import *
from enquiry.connect import *
from enquiry.secondary import *

# create new blueprint
forums_blueprint = Blueprint('forums', 'forums', url_prefix='/api/forum')

forum_service = ForumService()
forum_model = ForumModel
user_service = UserService()
user_model = UserModel
thread_service = ThreadService()
thread_model = ThreadModel
data_context = PostgresDataContext()
STATUS_CODE = {
	'OK': 200,
	'CREATED': 201,
	'NOT_FOUND': 404,
	'CONFLICT': 409
}


@forums_blueprint.route('/create', methods=['POST'])
def create_forum():
	content = request.get_json(silent=True)
	connect, cursor = data_context.create_connection()

	cursor.execute(SELECT_USERS_BY_NICKNAME, [content['user'] ])
	user = cursor.fetchone()
	if user is None:
		data_context.put_connection(connect)
		cursor.close()
		return make_response(jsonify({"message": "Can't find user with nickname: " + content['user']}),
		                     STATUS_CODE['NOT_FOUND'])

	try:
		cursor.execute(INSERT_FORUM, [user['user_id'], content['slug'], content['title'], user['nickname'] ])
		returning_forum = cursor.fetchone()
		data_context.put_connection(connect)
		cursor.close()
		return make_response(jsonify(returning_forum), STATUS_CODE['CREATED'])
	except:
		cursor.execute(SELECT_FORUM_BY_SLUG, [content['slug'], ])
		returning_forum = cursor.fetchone()
		data_context.put_connection(connect)
		cursor.close()
		return make_response(jsonify(returning_forum), STATUS_CODE['CONFLICT'])


@forums_blueprint.route('/<slug>/create', methods=['POST'])
def create_thread(slug):
	content = request.get_json(silent=True)
	connect, cursor = data_context.create_connection()

	cursor.execute(SELECT_USERS_BY_NICKNAME, [content['author']])
	user = cursor.fetchone()
	if user is None:
		data_context.put_connection(connect)
		cursor.close()
		return make_response(jsonify({"message": "Can't find user with nickname: " + content['author']}),
								STATUS_CODE['NOT_FOUND'])

	cursor.execute(SELECT_FORUM_BY_SLUG, [slug, ])
	forum = cursor.fetchone()
	if user is None:
		data_context.put_connection(connect)
		cursor.close()
		return make_response(jsonify({"message": "Can't find forum with slug: " + slug}),
								STATUS_CODE['NOT_FOUND'])

	try:
		command = '''INSERT INTO threads (forum_id, user_id, author, created, forum, message, slug, title) 
					VALUES (%s, %s, '%s', '%s', '%s', '%s', '%s', '%s')	RETURNING *;''' % (forum["forum_id"], user["user_id"], user["nickname"],
								   content["created"], forum["slug"], content["message"],
								   content["slug"], content["title"])

		cursor.execute(command)
		thread = cursor.fetchone()
		param_name_array = ["author", "created", "forum", "id", "message", "slug", "title"]
		param_value_array = [thread["author"], convert_time(thread["created"]),
							 thread["forum"], thread["thread_id"], thread["message"],
							 thread["slug"], thread["title"]]
		return make_response(jsonify(dict(zip(param_name_array, param_value_array))), STATUS_CODE['CREATED'])
	except:
		cursor.execute(SELECT_THREAD_BY_SLUG, content["slug"])
		thread = cursor.fetchone()
		param_name_array = ["author", "created", "forum", "id", "message", "slug", "title"]
		param_value_array = [thread["author"], convert_time(thread["created"]),
		                     thread["forum"], thread["thread_id"], thread["message"],
		                     thread["slug"], thread["title"]]
		return make_response(jsonify(dict(zip(param_name_array, param_value_array))), STATUS_CODE['CONFLICT'])
	finally:
		data_context.put_connection(connect)
		cursor.close()






	# user_content = dict()
	# forum_content = dict()
	# forum_content['slug'] = slug
	# user_content['nickname'] = content['author']
	# user = user_model.from_dict(user_content)
	# forum = forum_model.from_dict(forum_content)
	# thread = thread_model.from_dict(content)
	#
	# forum, user, message_or_thread, code = forum_service.create_thread(user, forum, thread)
	#
	# if code == STATUS_CODE['NOT_FOUND']:
	#
	# 	return make_response(jsonify(message_or_thread), code)
	#
	# if code == STATUS_CODE['CONFLICT']:
	# 	if message_or_thread.created is not None:
	# 		param_name_array = ["author", "created", "forum", "id", "message", "slug", "title"]
	# 		param_value_array = [user.nickname, convert_time(message_or_thread.created),
	# 								forum.slug, message_or_thread.id, message_or_thread.message,
	# 								message_or_thread.slug, message_or_thread.title]
	# 	else:
	# 		param_name_array = ["author", "forum", "id", "message", "slug", "title"]
	# 		param_value_array = [user.nickname, forum.slug,
	# 							message_or_thread.id, message_or_thread.message,
	# 							message_or_thread.slug, message_or_thread.title]
	#
	# 	exist_thread_data = dict(zip(param_name_array, param_value_array))
	#
	# 	return make_response(jsonify(exist_thread_data), code)
	#
	# if code == STATUS_CODE['CREATED']:
	# 	if message_or_thread.created is not None:
	# 		param_name_array = ["author", "created", "forum", "id", "message", "slug", "title"]
	# 		param_value_array = [user.nickname, convert_time(message_or_thread.created),
	# 								forum.slug, message_or_thread.id, message_or_thread.message,
	# 								message_or_thread.slug, message_or_thread.title]
	# 	else:
	# 		param_name_array = ["author", "forum", "id", "message", "slug", "title"]
	# 		param_value_array = [user.nickname, forum.slug,
	# 							message_or_thread.id, message_or_thread.message,
	# 							message_or_thread.slug, message_or_thread.title]
	#
	# 	created_thread_data = dict(zip(param_name_array, param_value_array))
	#
	# 	return make_response(jsonify(created_thread_data), code)


@forums_blueprint.route('/<slug>/details', methods=['GET'])
def get_forum_information(slug):

	message_or_forum, code = forum_service.select_forum_by_slug(slug)

	if code == STATUS_CODE['OK']:
		count_posts = forum_service.count_posts_by_forum_id(message_or_forum)
		count_threads = forum_service.count_threads_by_forum_id(message_or_forum)
		user, status_code = user_service.select_user_by_user_id(message_or_forum.user_id)

		param_name_array = ["posts", "slug", "threads", "title", "user"]
		param_value_array = [count_posts, message_or_forum.slug, count_threads, message_or_forum.title, user.nickname]
		exist_forum_data = dict(zip(param_name_array, param_value_array))

		return make_response(jsonify(exist_forum_data), code)

	if code == STATUS_CODE['NOT_FOUND']:

		return make_response(jsonify(message_or_forum), code)


@forums_blueprint.route('/<slug>/threads', methods=['GET'])
def get_list_of_thread(slug):
	parameters = request.args

	message_or_forum, code = forum_service.select_forum_by_slug(slug)

	if code == STATUS_CODE['OK']:
		threads, status_code = thread_service.select_threads_by_forum_id(message_or_forum, parameters)

		if status_code == STATUS_CODE['OK']:

			return make_response(jsonify(threads), code)

	if code == STATUS_CODE['NOT_FOUND']:

		return make_response(jsonify(message_or_forum), code)


@forums_blueprint.route('/<slug>/users', methods=['GET'])
def get_list_of_users(slug):
	params = request.args

	message_or_forum, code = forum_service.select_forum_by_slug(slug)

	if code == STATUS_CODE['OK']:
		message_or_users, code = user_service.select_users_arr(message_or_forum, params)

		if code == STATUS_CODE['OK']:
			param_name_array = ["about", "email", "fullname", "nickname"]

			user_arr = []
			for user in message_or_users:
				param_value_array = [user.about, user.email,
										user.fullname, user.nickname]
				user_data = dict(zip(param_name_array, param_value_array))
				user_arr.append(user_data)

			return make_response(jsonify(user_arr), code)
		else:
			return make_response(jsonify(message_or_users), code)

	if code == STATUS_CODE['NOT_FOUND']:
		return make_response(jsonify(message_or_forum), code)

