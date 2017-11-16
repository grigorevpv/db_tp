from flask import Blueprint, request, make_response, jsonify
from api.repositories.connect import PostgresDataContext
from api.repositories.ForumRepository.forum_queries_db import *
from api.repositories.ThreadRepository.thread_queries_db import *
from api.repositories.PostRepository.post_queries_db import *
from api.repositories.UserRepository.user_queries_db import *
from api.repositories.VoteRepository.vote_queries_db import *
from api.services.ForumService.ForumService import ForumService
from api.models.forums.ForumModel import ForumModel
from api.services.UserService.UserService import UserService
from api.models.users.UserModel import UserModel
from api.services.ThreadService.ThreadServise import ThreadService
from api.models.threads.ThreadModel import ThreadModel
from api.services.PostService.PostService import PostService
from api.models.posts.PostModel import PostModel
from api.services.VoteService.VoteService import VoteService
from enquiry.queries_db import *
from enquiry.connect import *
from enquiry.secondary import *

# create new blueprint
service_blueprint = Blueprint('service', 'service', url_prefix='/api/service')

forum_service = ForumService()
forum_model = ForumModel
user_service = UserService()
user_model = UserModel
thread_service = ThreadService()
thread_model = ThreadModel
post_service = PostService()
post_model = PostModel
vote_service = VoteService()
data_context = PostgresDataContext()
STATUS_CODE = {
	'OK': 200,
	'CREATED': 201,
	'NOT_FOUND': 404,
	'CONFLICT': 409
}


@service_blueprint.route('/status', methods=['GET'])
def get_information():
	connect, cursor = data_context.create_connection()

	cursor.execute(SELECT_COUNT_FORUMS)
	count_forums = cursor.fetchone()["forums_count"]
	cursor.execute(SELECT_COUNT_THREADS)
	count_threads = cursor.fetchone()["threads_count"]
	cursor.execute(SELECT_COUNT_POSTS)
	count_posts = cursor.fetchone()["posts_count"]
	cursor.execute(SELECT_COUNT_USERS)
	count_users = cursor.fetchone()["users_count"]

	param_name_array = ["forum", "post", "thread", "user"]
	param_value_array = [count_forums, count_posts, count_threads, count_users]
	bd_information = dict(zip(param_name_array, param_value_array))

	data_context.put_connection(connect)
	cursor.close()
	return make_response(jsonify(bd_information), STATUS_CODE['OK'])


@service_blueprint.route('/clear', methods=['POST'])
def clear_tables():
	connect, cursor = data_context.create_connection()

	cursor.execute(DELETE_FORUMS_TABLE)
	cursor.execute(DELETE_THREADS_TABLE)
	cursor.execute(DELETE_POSTS_TABLE)
	cursor.execute(DELETE_USERS_TABLE)
	cursor.execute(DELETE_VOTES_TABLE)

	data_context.put_connection(connect)
	cursor.close()
	return make_response(jsonify(None), STATUS_CODE['OK'])

