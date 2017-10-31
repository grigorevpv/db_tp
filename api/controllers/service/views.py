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
service_blueprint = Blueprint('service', 'service', url_prefix='/service')

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


@service_blueprint.route('/status', methods=['GET'])
def get_information():
	count_forums, code = forum_service.count_forums()
	count_threads, code = thread_service.count_threads()
	count_posts, code = post_service.count_posts()
	count_users, code = user_service.count_users()

	param_name_array = ["forum", "post", "thread", "user"]
	param_value_array = [count_forums, count_posts, count_threads, count_users]
	bd_information = dict(zip(param_name_array, param_value_array))

	return make_response(jsonify(bd_information), STATUS_CODE['OK'])

