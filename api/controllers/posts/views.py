from flask import Blueprint, request, make_response, jsonify
from api.services.ForumService.ForumService import ForumService
from api.models.forums.ForumModel import ForumModel
from api.services.UserService.UserService import UserService
from api.models.users.UserModel import UserModel
from api.services.ThreadService.ThreadServise import ThreadService
from api.models.threads.ThreadModel import ThreadModel
from api.services.PostService.PostService import PostService
from api.models.posts.PostModel import PostModel
from enquiry.queries_db import *
from enquiry.connect import *
from enquiry.secondary import *

# create new blueprint
posts_blueprint = Blueprint('posts', 'posts', url_prefix='/api/post')

forum_service = ForumService()
forum_model = ForumModel
user_service = UserService()
user_model = UserModel
thread_service = ThreadService()
thread_model = ThreadModel
post_service = PostService()
post_model = PostModel
STATUS_CODE = {
	'OK': 200,
	'CREATED': 201,
	'NOT_FOUND': 404,
	'CONFLICT': 409
}


@posts_blueprint.route('/<id>/details', methods=['GET'])
def get_post_details_get(id):
	params = request.args.getlist('related')

	message_or_post, code = post_service.select_post_by_id(id)

	if code == STATUS_CODE['OK']:
		message_or_user, code = user_service.select_user_by_user_id(message_or_post.user_id)
		message_or_forum, code = forum_service.select_forum_by_id(message_or_post.forum_id)
		user, forum, thread, post = ({}, {}, {}, {})
		for val in params:
			for key in val.split(','):
				if 'user' == key:
					param_name_array = ["about", "email", "fullname", "nickname"]
					param_value_array = [message_or_user.about, message_or_user.email,
										message_or_user.fullname, message_or_user.nickname]
					user = dict(zip(param_name_array, param_value_array))
				if 'forum' == key:
					count_posts = forum_service.count_posts_by_forum_id(message_or_forum)
					count_threads = forum_service.count_threads_by_forum_id(message_or_forum)
					forum_user, code = user_service.select_user_by_user_id(message_or_forum.user_id)
					param_name_array = ["posts", "slug", "threads", "title", "user"]
					param_value_array = [count_posts, message_or_forum.slug, count_threads,
										message_or_forum.title, forum_user.nickname]
					forum = dict(zip(param_name_array, param_value_array))
				if 'thread' == key:
					message_or_thread, code = thread_service.select_thread_by_id(message_or_post.thread_id)
					thread_user, code = user_service.select_user_by_user_id(message_or_thread.user_id)
					param_name_array = ["author", "created", "forum", "id", "message", "slug", "title"]
					param_value_array = [thread_user.nickname, convert_time(message_or_thread.created),
										message_or_forum.slug, message_or_thread.id, message_or_thread.message,
										message_or_thread.slug, message_or_thread.title]
					thread = dict(zip(param_name_array, param_value_array))

		param_name_array = ["author", "created", "forum", "id", "isEdited", "message", "parent", "thread"]
		param_value_array = [message_or_user.nickname, convert_time(message_or_post.created),
							message_or_forum.slug, message_or_post.id, message_or_post.isedited,
							message_or_post.message, message_or_post.parent_id, message_or_post.thread_id]
		post = dict(zip(param_name_array, param_value_array))

		post_data = dict()

		if len(user) != 0:
			post_data['author'] = user
		if len(forum) != 0:
			post_data['forum'] = forum
		if len(thread) != 0:
			post_data['thread'] = thread
		post_data['post'] = post

		return make_response(jsonify(post_data), code)

	if code == STATUS_CODE['NOT_FOUND']:
		return make_response(jsonify(message_or_post), code)


@posts_blueprint.route('/<id>/details', methods=['POST'])
def get_post_details_post(id):
	content = request.get_json(silent=True)

	message_or_post, code = post_service.select_post_by_id(id)

	if code == STATUS_CODE['OK']:
		if 'message' in content:
			if message_or_post.message != content['message']:
				message_or_post, code = post_service.update_post(message_or_post, content['message'])

		if code == STATUS_CODE['OK']:
			message_or_user, code = user_service.select_user_by_user_id(message_or_post.user_id)
			message_or_forum, code = forum_service.select_forum_by_id(message_or_post.forum_id)
			param_name_array = ["author", "created", "forum", "id", "isEdited", "message", "parent", "thread"]
			param_value_array = [message_or_user.nickname, convert_time(message_or_post.created),
			                     message_or_forum.slug, message_or_post.id, message_or_post.isedited,
			                     message_or_post.message, message_or_post.parent_id, message_or_post.thread_id]
			post = dict(zip(param_name_array, param_value_array))
			return make_response(jsonify(post), code)

	if code == STATUS_CODE['NOT_FOUND']:
		return make_response(jsonify(message_or_post), code)



