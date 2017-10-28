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
from enquiry.queries_db import *
from enquiry.connect import *
from enquiry.secondary import *

# create new blueprint
threads_blueprint = Blueprint('threads', 'threads', url_prefix='/thread')

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
STATUS_CODE = {
	'OK': 200,
	'CREATED': 201,
	'NOT_FOUND': 404,
	'CONFLICT': 409
}

@threads_blueprint.route('/<slug_or_id>/create', methods=['POST'])
def create_posts(slug_or_id):
	content = request.get_json(silent=True)

	message_or_thread, code = thread_service.select_thread_by_slug_or_id(slug_or_id)

	if code == STATUS_CODE['OK']:
		created_threads_arr = []
		created_time = datetime.now()

		for post in content:
			user, status_code = user_service.select_user_by_nickname(post['author'])
			forum, status_code = forum_service.select_forum_by_id(message_or_thread.forum_id)

			path = list()
			post_content = dict()
			post_content['user_id'] = user.id
			post_content['thread_id'] = message_or_thread.id
			post_content['forum_id'] = message_or_thread.forum_id
			post_content['created'] = created_time
			post_content['message'] = post['message']
			if post.get('parent') is not None:
				post_content['parent_id'] = post['parent']
			else:
				post_content['parent_id'] = 0
			post_content['path'] = path
			post = post_model.from_dict(post_content)

			created_post, status_code = post_service.create_post(post)

			param_name_array = ["author", "created", "forum", "id", "isEdited", "message",
								"parent", "thread"]
			param_value_array = [user.nickname, convert_time(created_post.created), forum.slug, created_post.id, created_post.isedited,
			                     created_post.message, created_post.parent_id, message_or_thread.id]
			created_thread_data = dict(zip(param_name_array, param_value_array))
			created_threads_arr.append(created_thread_data)

		return make_response(jsonify(created_threads_arr), STATUS_CODE['CREATED'])
	if code == STATUS_CODE['NOT_FOUND']:

		return make_response(jsonify(message_or_thread), code)


@threads_blueprint.route('/<slug_or_id>/vote', methods=['POST'])
def create_vote(slug_or_id):
	content = request.get_json(silent=True)
	user_content = dict()
	user_content['nickname'] = content['nickname']
	user = user_model.from_dict(user_content)
	vote = vote_model.from_dict(content)

	message_or_thread, code = thread_service.select_thread_by_slug_or_id(slug_or_id)

	if code == STATUS_CODE['OK']:
		thread, user, message_or_vote, code = vote_service.create_vote(message_or_thread, user, vote)
		if code == STATUS_CODE['NOT_FOUND']:

			return make_response(jsonify(message_or_vote), code)
		if code == STATUS_CODE['OK']:
			forum, status_code = forum_service.select_forum_by_id(thread.forum_id)
			count_votes, status_code = vote_service.count_votes_by_thread_id(thread.id)
			user, status_code = user_service.select_user_by_user_id(thread.user_id)

			if thread.created is not None:
				param_name_array = ["author", "created", "forum", "id", "message", "slug", "title", "votes"]
				param_value_array = [user.nickname, convert_time(thread.created),
				                     forum.slug, thread.id, thread.message,
				                     thread.slug, thread.title, count_votes]
			else:
				param_name_array = ["author", "forum", "id", "message", "slug", "title", "votes"]
				param_value_array = [user.nickname, forum.slug,
				                     message_or_thread.id, message_or_thread.message,
				                     message_or_thread.slug, message_or_thread.title, count_votes]

			thread_data = dict(zip(param_name_array, param_value_array))

			return make_response(jsonify(thread_data), code)

	if code == STATUS_CODE['NOT_FOUND']:

		return make_response(jsonify(message_or_thread), code)

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

@threads_blueprint.route('/<slug_or_id>/posts', methods=['GET'])
def get_posts_information(slug_or_id):
	params = request.args
	message_or_thread, code = thread_service.select_thread_by_slug_or_id(slug_or_id)

	if code == STATUS_CODE['OK']:
		message_or_posts_arr, code = post_service.get_posts_arr(message_or_thread, params)

	if code == STATUS_CODE['NOT_FOUND']:
		return make_response(jsonify(message_or_thread), code)





