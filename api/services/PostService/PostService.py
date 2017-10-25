from api.repositories.ForumRepository.ForumRepository import ForumRepository
from api.repositories.UserRepository.UserRepository import UserRepository
from api.repositories.PostRepository.PostRepository import PostRepository

user_repository = UserRepository()
forum_repository = ForumRepository()
post_repository = PostRepository()

STATUS_CODE = {
	'OK': 200,
	'CREATED': 201,
	'NOT_FOUND': 404,
	'CONFLICT': 409
}

class PostService(object):

	@staticmethod
	def create_post(post):
		try:
			post = post_repository.create_post(post)

			return post, STATUS_CODE['CREATED']
		except:
			message = {"message": "Post didn't created"}

			return message, STATUS_CODE['CONFLICT']
