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
posts_blueprint = Blueprint('posts', 'posts', url_prefix='/post')

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

