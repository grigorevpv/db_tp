from datetime import datetime
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
threads_blueprint = Blueprint('threads', 'threads', url_prefix='/thread')

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

@threads_blueprint.route('/<slug_or_id>/create', methods=['POST'])
def create_posts(slug_or_id):
	content = request.get_json(silent=True)

	message_or_thread, code = thread_service.select_thread_by_slug_or_id(slug_or_id)

	if code == STATUS_CODE['OK']:
		created_threads_arr = []

		for post in content:
			user, status_code = user_service.select_user_by_nickname(post['author'])
			forum, status_code = forum_service.select_forum_by_id(message_or_thread.forum_id)
			post_content = dict()
			post_content['user_id'] = user.id
			post_content['thread_id'] = message_or_thread.id
			post_content['forum_id'] = message_or_thread.forum_id
			post_content['created'] = datetime.now()
			post_content['message'] = post['message']
			post_content['parent_id'] = 0 if post.get('parent') is None else post['parent_id']
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