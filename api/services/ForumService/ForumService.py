from api.repositories.ForumRepository.ForumRepository import ForumRepository
from api.repositories.UserRepository.UserRepository import UserRepository
from api.repositories.ThreadRepository.ThreadRepository import ThreadRepository

user_repository = UserRepository()
forum_repository = ForumRepository()
thread_repository = ThreadRepository()

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
	def select_forum_by_slug(forum_slug):
		try:
			forum = forum_repository.select_forum_by_slug(forum_slug)

			return forum, STATUS_CODE['OK']
		except:
			message = {"message": "Can't find forum with slug: " + forum_slug}

			return message, STATUS_CODE['NOT_FOUND']

	@staticmethod
	def select_forum_by_id(forum_id):
		try:
			forum = forum_repository.select_forum_by_id(forum_id)

			return forum, STATUS_CODE['OK']
		except:
			message = {"message": "Can't find forum with id: " + forum_id}

			return message, STATUS_CODE['NOT_FOUND']

	@staticmethod
	def create_thread(user, forum, thread):

		try:
			message_or_user = user_repository.select_user_by_nickname(user.nickname)
		except:
			message = {"message": "Can't find user with nickname: " + user.nickname}

			return forum, user, message, STATUS_CODE['NOT_FOUND']

		try:
			message_or_forum = forum_repository.select_forum_by_slug(forum.slug)
		except:
			message = {"message": "Can't find forum with slug: " + forum.slug}

			return forum, user, message, STATUS_CODE['NOT_FOUND']

		try:
			message_or_thread = thread_repository.get_thread_by_slug(thread.slug)
			message_or_user = user_repository.select_user_by_user_id(message_or_thread.user_id)
			message_or_forum = forum_repository.select_forum_by_id(message_or_thread.forum_id)

			return message_or_forum, message_or_user, message_or_thread, STATUS_CODE['CONFLICT']

		except:

			message_or_thread = forum_repository.create_thread(thread, message_or_forum, message_or_user)

			return message_or_forum, message_or_user, message_or_thread, STATUS_CODE['CREATED']

	@staticmethod
	def count_forums():

		try:
			message_or_count = forum_repository.count_forums()
			return message_or_count, STATUS_CODE['OK']
		except:
			message = {"message": "Forums is not exist"}
			return message, STATUS_CODE['NOT_FOUND']






