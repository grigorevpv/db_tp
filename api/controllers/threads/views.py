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

		for post in content:
			user, code = user_service.select_user_by_nickname(post['author'])
			forum, code = forum_service.select_forum_bu_slug(message_or_thread.forum_id)
			post_content = dict()
			post_content['user_id'] = user.id
			post_content['thread_id'] = message_or_thread.id
			post_content['forum_id'] = message_or_thread.forum_id
			post_content['created'] = convert_time(datetime.now())
			post_content['message'] = content['message']
			post_content['parent_id'] = 0 if content.get('parent') is None else content['parent_id']
			post = post_model.from_dict(post_content)

			post, code = post_service.create_post(post)


		return make_response(jsonify(message_or_thread), code)
	if code == STATUS_CODE['NOT_FOUND']:

		return make_response(jsonify(message_or_thread), code)