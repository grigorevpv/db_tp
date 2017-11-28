from flask import Blueprint, request, make_response, jsonify
from api.repositories.connect import PostgresDataContext
from api.repositories.ForumRepository.forum_queries_db import *
from api.repositories.UserRepository.user_queries_db import *
from enquiry.queries_db import *
from enquiry.secondary import *

# create new blueprint
forums_blueprint = Blueprint('forums', 'forums', url_prefix='/api/forum')

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
	if forum is None:
		data_context.put_connection(connect)
		cursor.close()
		return make_response(jsonify({"message": "Can't find forum with slug: " + slug}),
								STATUS_CODE['NOT_FOUND'])

	if content.get("slug") is not None:
		cursor.execute( SELECT_THREAD_BY_SLUG, [content["slug"], ] )
		returning_thread = cursor.fetchone()
		if returning_thread is not None:
			returning_thread[ 'created' ] = convert_time( returning_thread[ 'created' ] )
			data_context.put_connection( connect )
			cursor.close()
			return make_response( jsonify( returning_thread ),
			                      STATUS_CODE[ 'CONFLICT' ] )
	else:
		content[ "slug" ] = ""

	if content.get("created") is None:
		command = '''INSERT INTO threads (forum_id, user_id, author, forum, message, slug, title)
							VALUES (%s, %s, '%s', '%s', '%s', '%s', '%s')	RETURNING id, author, created, forum, message, slug, title;''' % \
		          (forum["forum_id"], user["user_id"], user["nickname"],
					forum["slug"], content["message"], content["slug"], content["title"])
	else:
		command = '''INSERT INTO threads (forum_id, user_id, author, created, forum, message, slug, title)
				VALUES (%s, %s, '%s', '%s', '%s', '%s', '%s', '%s')	RETURNING id, author, created, forum, message, slug, title;''' % (forum["forum_id"], user["user_id"], user["nickname"],
	                    content["created"], forum["slug"], content["message"],
							   content["slug"], content["title"])

	cursor.execute(command)
	thread = cursor.fetchone()
	thread['created'] = convert_time(thread['created'])

	data_context.put_connection( connect )
	cursor.close()
	return make_response(jsonify(thread), STATUS_CODE['CREATED'])



@forums_blueprint.route('/<slug>/details', methods=['GET'])
def get_forum_information(slug):
	params = request.args
	connect, cursor = data_context.create_connection()

	cursor.execute(SELECT_FORUM_BY_SLUG, [slug, ])
	forum = cursor.fetchone()
	if forum is None:
		data_context.put_connection(connect)
		cursor.close()
		return make_response(jsonify({"message": "Can't find forum with slug: " + slug}),
		                     STATUS_CODE['NOT_FOUND'])

	# cursor.execute(SELECT_COUNT_POSTS_BY_FORUM_ID, [forum["forum_id"], ])
	# count_posts = cursor.fetchone()["posts_count"]
	# forum["posts"] = count_posts
	#
	# cursor.execute(SELECT_COUNT_THREADS_BY_FORUM_ID, [forum["forum_id"], ])
	# count_threads = cursor.fetchone()["threads_count"]
	# forum["threads"] = count_threads

	data_context.put_connection(connect)
	cursor.close()
	return make_response(jsonify(forum), STATUS_CODE['OK'])


@forums_blueprint.route('/<slug>/threads', methods=['GET'])
def get_list_of_thread(slug):
	params= request.args
	connect, cursor = data_context.create_connection()

	cursor.execute( SELECT_FORUM_BY_SLUG, [ slug, ] )
	forum = cursor.fetchone()
	if forum is None:
		data_context.put_connection( connect )
		cursor.close()
		return make_response( jsonify( {"message": "Can't find forum with slug: " + slug} ),
		                      STATUS_CODE[ 'NOT_FOUND' ] )

	limit = ' ALL '
	if 'limit' in params:
		limit = params.get( 'limit' )
	order = 'asc'
	if 'desc' in params:
		order = 'desc' if params.get( 'desc' ) == 'true' else 'asc'
	since = ''
	if 'since' in params:
		znak = ' <= ' if order == 'desc' else ' >= '
		time = " '%s' " % (params.get( 'since' ))
		since = 'and created ' + znak + time

	order = ' ' + order + ' '

	command = SELECT_THREADS_BY_FORUM_ID % (forum["forum_id"], since, order, limit)
	cursor.execute(command)
	threads = cursor.fetchall()
	threads_arr = []

	for thread in threads:
		thread["created"] = convert_time(thread["created"])
		threads_arr.append(thread)

	data_context.put_connection( connect )
	cursor.close()
	return make_response(jsonify(threads_arr), STATUS_CODE['OK'])


@forums_blueprint.route('/<slug>/users', methods=['GET'])
def get_list_of_users(slug):
	params = request.args
	connect, cursor = data_context.create_connection()

	cursor.execute(SELECT_FORUM_BY_SLUG, [slug, ])
	forum = cursor.fetchone()
	if forum is None:
		data_context.put_connection(connect)
		cursor.close()
		return make_response(jsonify({"message": "Can't find forum with slug: " + slug}),
		                     STATUS_CODE['NOT_FOUND'])

	users, limit, since, desc = None, 100, None, False

	if 'limit' in params:
		limit = params.get('limit')
	if 'desc' in params:
		if params.get('desc') == 'true':
			desc = True
	if 'since' in params:
		since = params.get('since')

	if since is not None:
		if desc:
			command = SELECT_USERS_SINCE_DESC % (forum["forum_id"], forum["forum_id"], since, limit)
			cursor.execute(command)
			users = cursor.fetchall()
		else:
			command = SELECT_USERS_SINCE % (forum["forum_id"], forum["forum_id"], since, limit)
			cursor.execute(command)
			users = cursor.fetchall()

	else:
		if desc:
			command = SELECT_USERS_DESC % (forum["forum_id"], forum["forum_id"], limit)
			cursor.execute(command)
			users = cursor.fetchall()
			if users is None:
				raise Exception("user is not exist")
		else:
			command = '''SELECT * FROM users WHERE user_id IN (SELECT u.user_id FROM posts p
                 JOIN users u ON p.user_id = u.user_id
                 WHERE forum_id = %s
                 UNION
                 SELECT us.user_id FROM threads th
                 JOIN users us ON th.user_id = us.user_id
                 WHERE forum_id = %s)
                 ORDER BY users.nickname COLLATE ucs_basic 
                 LIMIT %s;''' % (forum["forum_id"], forum["forum_id"], limit)
			cursor.execute(command)
			users = cursor.fetchall()

	if users is None:
		data_context.put_connection(connect)
		cursor.close()
		return make_response(jsonify({"message": "Can't find users"}),
		                     STATUS_CODE['NOT_FOUND'])

	users_arr = []
	for user in users:
		users_arr.append(user)

	data_context.put_connection(connect)
	cursor.close()
	return make_response(jsonify(users_arr), STATUS_CODE['OK'])


