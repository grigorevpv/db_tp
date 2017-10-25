from api.repositories.ForumRepository.ForumRepository import ForumRepository
from api.repositories.UserRepository.UserRepository import UserRepository

user_repository = UserRepository()
forum_repository = ForumRepository()

STATUS_CODE = {
	'OK': 200,
	'CREATED': 201,
	'NOT_FOUND': 404,
	'CONFLICT': 409
}

class ForumService(object):

	@staticmethod
	def create_forum(forum, user):
		try:
			forum = forum_repository.create_forum(forum, user)
		except:
			message = {"message": "Forum with is exist slug =" + forum.slug}

			return message, STATUS_CODE['CONFLICT']

		return forum, STATUS_CODE['CREATED']

	@staticmethod
	def count_posts_by_forum_id(forum):
		try:
			count_posts = forum_repository.count_posts_by_forum_id(forum)

			return count_posts
		except:
			print("[ForumService] count_posts_by_forum_id exception")

	@staticmethod
	def count_threads_by_forum_id(forum):
		try:
			count_threads = forum_repository.count_threads_by_forum_id(forum)

			return count_threads
		except:
			print("[ForumService] count_posts_by_forum_id exception")

	@staticmethod
	def select_forum_by_id(forum_id):
		try:
			forum = forum_repository.select_forum_by_id(forum_id)

			return forum, STATUS_CODE['OK']
		except:
			message = {"message": "Can't find forum with id: " + forum_id}

			return message, STATUS_CODE['NOT_FOUND']

	@staticmethod
	def create_thread(thread, forum, user):
		try:
			thread = forum_repository.create_thread(thread, forum, user)

			return thread, STATUS_CODE['CREATED']
		except:
			print("[ForumService] create_thread exception")

			return thread, STATUS_CODE['CONFLICT']

