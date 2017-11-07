from datetime import datetime
from flask import Blueprint, request, make_response, jsonify
from api.services.ForumService.ForumService import ForumService
from api.models.forums.ForumModel import ForumModel
from api.services.UserService.UserService import UserService
from api.models.users.UserModel import UserModel
from api.services.ThreadService.ThreadServise import ThreadService
from api.models.threads.ThreadModel import ThreadModel
from api.services.VoteService.VoteService import VoteService
from api.models.votes.VoteModel import VoteModel
from api.services.PostService.PostService import PostService
from api.models.posts.PostModel import PostModel
from api.repositories.connect import PostgresDataContext
from api.repositories.ThreadRepository.thread_queries_db import *
from api.repositories.PostRepository.post_queries_db import *
from api.repositories.VoteRepository.vote_queries_db import *
from enquiry.queries_db import *
from enquiry.connect import *
from enquiry.secondary import *

# create new blueprint
threads_blueprint = Blueprint('threads', 'threads', url_prefix='/api/thread')

forum_service = ForumService()
forum_model = ForumModel
user_service = UserService()
user_model = UserModel
thread_service = ThreadService()
thread_model = ThreadModel
post_service = PostService()
post_model = PostModel
vote_service = VoteService()
vote_model = VoteModel
data_context = PostgresDataContext()
STATUS_CODE = {
	'OK': 200,
	'CREATED': 201,
	'NOT_FOUND': 404,
	'CONFLICT': 409
}


@threads_blueprint.route('/<slug_or_id>/create', methods=['POST'])
def create_posts(slug_or_id):
	content = request.get_json(silent=True)
	connect, cursor = data_context.create_connection()

	if slug_or_id.isdigit():
		cursor.execute(SELECT_THREAD_BY_ID, [slug_or_id, ])
		thread = cursor.fetchone()
		if thread is None:
			data_context.put_connection(connect)
			cursor.close()
			return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
								 STATUS_CODE['NOT_FOUND'])
	else:
		cursor.execute(SELECT_THREAD_BY_SLUG, [slug_or_id, ])
		thread = cursor.fetchone()
		if thread is None:
			data_context.put_connection(connect)
			cursor.close()
			return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
								 STATUS_CODE['NOT_FOUND'])

	created_threads_arr = []
	created_time = datetime.now()

	for post in content:
		cursor.execute(SELECT_USERS_BY_NICKNAME, [post['author']])
		user = cursor.fetchone()
		if user is None:
			data_context.put_connection(connect)
			cursor.close()
			return make_response(jsonify({"message": "Can't find user with nickname: " + post['author']}),
								 STATUS_CODE['NOT_FOUND'])

		cursor.execute(SELECT_FORUM_BY_FORUM_ID, [thread["forum_id"]])
		forum = cursor.fetchone()
		if user is None:
			data_context.put_connection(connect)
			cursor.close()
			return make_response(jsonify({"message": "Can't find forum with forum_id: " + thread["forum_id"]}),
								 STATUS_CODE['NOT_FOUND'])

		post_path = list()
		parent_id = 0
		if post.get('parent') is not None:
			parent_id = post['parent']
			cursor.execute(SELECT_POST_BY_ID, [post['parent'], ])
			parent_post = cursor.fetchone()
			if post is None:
				data_context.put_connection(connect)
				cursor.close()
				return make_response(jsonify({"message": "Didn't find post with id: " + post['parent']}),
				                     STATUS_CODE['NOT_FOUND'])
			else:
				post_path.extend(parent_post["path"])

		cursor.execute(SELECT_NEXT_VAL)
		post_id = cursor.fetchone()["nextval"]
		post_path.append(post_id)
		cursor.execute(INSERT_POST, [post_id, user["user_id"], thread["id"], forum["forum_id"], parent_id, created_time,
		                  post["message"], post_path, ])
		returning_post = cursor.fetchone()
		param_name_array = ["author", "created", "forum", "id", "isEdited", "message",
		                     "parent", "thread"]
		param_value_array = [user["nickname"],
		                     convert_time(created_time),
		                     forum["slug"],
		                     returning_post["post_id"],
		                      returning_post["isedited"],
		                     returning_post["message"],
		                     returning_post["parent_id"],
		                     thread["id"]]
		created_thread_data = dict(zip( param_name_array, param_value_array))
		created_threads_arr.append(created_thread_data)

	return make_response(jsonify(created_threads_arr), STATUS_CODE['CREATED'])


@threads_blueprint.route('/<slug_or_id>/vote', methods=['POST'])
def create_vote(slug_or_id):
	content = request.get_json(silent=True)
	connect, cursor = data_context.create_connection()

	if slug_or_id.isdigit():
		cursor.execute(SELECT_THREAD_BY_ID, [slug_or_id, ])
		thread = cursor.fetchone()
		if thread is None:
			data_context.put_connection(connect)
			cursor.close()
			return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
								 STATUS_CODE['NOT_FOUND'])
	else:
		cursor.execute(SELECT_THREAD_BY_SLUG, [slug_or_id, ])
		thread = cursor.fetchone()
		if thread is None:
			data_context.put_connection(connect)
			cursor.close()
			return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
								 STATUS_CODE['NOT_FOUND'])

	cursor.execute(SELECT_USERS_BY_NICKNAME, [content['nickname']])
	user = cursor.fetchone()
	if user is None:
		data_context.put_connection(connect)
		cursor.close()
		return make_response(jsonify({"message": "Can't find user with nickname: " + post['author']}),
		                     STATUS_CODE['NOT_FOUND'])

	cursor.execute(SELECT_VOTE_BY_THREAD_AND_USER_ID, [thread["id"], user["user_id"]])
	vote = cursor.fetchone()
	if vote is None:
		cursor.execute(INSERT_VOTE, [user["user_id"], thread["id"], content["voice"], ])
		vote = cursor.fetchone()
	else:
		if vote["voice"] != content["voice"]:
			cursor.execute(UPDATE_VOTE, [content["voice"], user["user_id"], thread["id"], ])
			vote = cursor.fetchone()

	cursor.execute(COUNT_VOTES_BY_THREAD_ID, [thread["id"], ])
	count_votes = cursor.fetchone()["votes_count"]

	thread["votes"] = count_votes
	thread["created"] = convert_time(thread["created"])

	data_context.put_connection(connect)
	cursor.close()
	return make_response(jsonify(thread), STATUS_CODE['OK'])


# @threads_blueprint.route('/<slug_or_id>/vote', methods=['POST'])
# def create_vote(slug_or_id):
# 	content = request.get_json(silent=True)
# 	user_content = dict()
# 	user_content['nickname'] = content['nickname']
# 	user = user_model.from_dict(user_content)
# 	vote = vote_model.from_dict(content)
#
# 	message_or_thread, code = thread_service.select_thread_by_slug_or_id(slug_or_id)
#
# 	if code == STATUS_CODE['OK']:
# 		thread, user, message_or_vote, code = vote_service.create_vote(message_or_thread, user, vote)
#
# 		if code == STATUS_CODE['NOT_FOUND']:
# 			return make_response(jsonify(message_or_vote), code)
# 		if code == STATUS_CODE['OK']:
# 			forum, status_code = forum_service.select_forum_by_id(thread.forum_id)
# 			count_votes, status_code = vote_service.count_votes_by_thread_id(thread.id)
# 			message_or_user, status_code = user_service.select_user_by_user_id(thread.user_id)
# 			if status_code == STATUS_CODE['NOT_FOUND']:
# 				return make_response(jsonify(message_or_user), status_code)
#
# 			if thread.created is not None:
# 				param_name_array = ["author", "created", "forum", "id", "message", "slug", "title", "votes"]
# 				param_value_array = [message_or_user.nickname, convert_time(thread.created),
# 				                     forum.slug, thread.id, thread.message,
# 				                     thread.slug, thread.title, count_votes]
# 			else:
# 				param_name_array = ["author", "forum", "id", "message", "slug", "title", "votes"]
# 				param_value_array = [message_or_user.nickname, forum.slug,
# 				                     message_or_thread.id, message_or_thread.message,
# 				                     message_or_thread.slug, message_or_thread.title, count_votes]
#
# 			thread_data = dict(zip(param_name_array, param_value_array))
#
# 			return make_response(jsonify(thread_data), code)
#
# 	if code == STATUS_CODE['NOT_FOUND']:
#
# 		return make_response(jsonify(message_or_thread), code)


@threads_blueprint.route('/<slug_or_id>/details', methods=['GET'])
def get_thread_information(slug_or_id):
	message_or_thread, code = thread_service.select_thread_by_slug_or_id(slug_or_id)

	if code == STATUS_CODE['OK']:
		user, status_code = user_service.select_user_by_user_id(message_or_thread.user_id)
		forum, status_code = forum_service.select_forum_by_id(message_or_thread.forum_id)
		try:
			count_votes, status_code = vote_service.count_votes_by_thread_id(message_or_thread.id)
		except:
			count_votes = 0

		if message_or_thread.created is not None:
			param_name_array = ["author", "created", "forum", "id", "message", "slug", "title", "votes"]
			param_value_array = [user.nickname, convert_time(message_or_thread.created),
			                     forum.slug, message_or_thread.id, message_or_thread.message,
			                     message_or_thread.slug, message_or_thread.title, count_votes]
		else:
			param_name_array = ["author", "forum", "id", "message", "slug", "title", "votes"]
			param_value_array = [user.nickname, forum.slug,
			                     message_or_thread.id, message_or_thread.message,
			                     message_or_thread.slug, message_or_thread.title, count_votes]

		thread_data = dict(zip(param_name_array, param_value_array))

		return make_response(jsonify(thread_data), code)

	if code == STATUS_CODE['NOT_FOUND']:
		return make_response(jsonify(message_or_thread), code)


@threads_blueprint.route('/<slug_or_id>/details', methods=['POST'])
def update_thread_information(slug_or_id):
	content = request.get_json(silent=True)
	thread_content = dict()
	if 'message' in content:
		thread_content['message'] = content['message']
	if 'title' in content:
		thread_content['title'] = content['title']

	message_or_thread, code = thread_service.select_thread_by_slug_or_id(slug_or_id)

	if code == STATUS_CODE['OK']:
		thread = thread_model.from_dict(thread_content)
		message_or_thread, code = thread_service.update_thread(message_or_thread, thread)
		if code == STATUS_CODE['OK']:
			user, status_code = user_service.select_user_by_user_id(message_or_thread.user_id)
			forum, status_code = forum_service.select_forum_by_id(message_or_thread.forum_id)
			param_name_array = ["author", "created", "forum", "id", "message", "slug", "title"]
			param_value_array = [user.nickname, convert_time(message_or_thread.created),
			                     forum.slug, message_or_thread.id, message_or_thread.message,
			                     message_or_thread.slug, message_or_thread.title]
			thread_data = dict(zip(param_name_array, param_value_array))
			return make_response(jsonify(thread_data), code)

	if code == STATUS_CODE['NOT_FOUND']:
		return make_response(jsonify(message_or_thread), code)


@threads_blueprint.route('/<slug_or_id>/posts', methods=['GET'])
def get_posts_information(slug_or_id):
	params = request.args
	message_or_thread, code = thread_service.select_thread_by_slug_or_id(slug_or_id)

	if code == STATUS_CODE['OK']:
		forum, code = forum_service.select_forum_by_id(message_or_thread.forum_id)
		message_or_posts_arr, code = post_service.get_posts_arr(message_or_thread, params)
		posts_arr = []
		param_name_array = ["author", "created", "forum", "id", "message", "parent", "thread"]

		for post in message_or_posts_arr:
			user, status_code = user_service.select_user_by_user_id(post.user_id)
			param_value_array = [user.nickname, convert_time(post.created), forum.slug,
			                     post.id, post.message, post.parent_id, post.thread_id]
			post = dict(zip(param_name_array, param_value_array))
			posts_arr.append(post)

		return make_response(jsonify(posts_arr), code)

	if code == STATUS_CODE['NOT_FOUND']:
		return make_response(jsonify(message_or_thread), code)





