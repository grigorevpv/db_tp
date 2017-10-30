from api.repositories.ForumRepository.ForumRepository import ForumRepository
from api.repositories.UserRepository.UserRepository import UserRepository
from api.repositories.ThreadRepository.ThreadRepository import ThreadRepository
from enquiry.secondary import *

user_repository = UserRepository()
forum_repository = ForumRepository()
thread_repository = ThreadRepository()

STATUS_CODE = {
	'OK': 200,
	'CREATED': 201,
	'NOT_FOUND': 404,
	'CONFLICT': 409
}


class ThreadService(object):
	@staticmethod
	def select_threads_by_forum_id(forum, params):
		limit = ' ALL '
		if 'limit' in params:
			limit = params.get('limit')
		order = 'asc'
		if 'desc' in params:
			order = 'desc' if params.get('desc') == 'true' else 'asc'
		since = ''
		if 'since' in params:
			znak = ' <= ' if order == 'desc' else ' >= '
			since = 'and created ' + znak + "'" + params.get('since') + "'"

		order = ' ' + order + ' '

		new_params = dict()
		new_params['limit'] = limit
		new_params['order'] = order
		new_params['since'] = since

		try:
			threads = thread_repository.select_threads_by_forum_id(forum, new_params)

			threads_arr = []
			param_name_array = ['author', 'created', 'forum', 'id', 'message', 'slug', 'title', 'votes']
			for thread in threads:
				user = user_repository.select_user_by_user_id(thread.user_id)
				count_votes = thread_repository.count_votes_by_thread_id(thread.id)
				threads_arr.append(dict(zip(param_name_array, [user.nickname, convert_time(thread.created), forum.slug, thread.id,
																thread.message, thread.slug, thread.title, count_votes])))

			return threads_arr, STATUS_CODE['OK']
		except:
			print("[ThreadService] select_threads_by_forum_id: Threads is no exist")

			return forum, STATUS_CODE['NOT_FOUND']

	@staticmethod
	def select_thread_by_slug_or_id(slug_or_id):
		if slug_or_id.isdigit():
			try:
				thread = thread_repository.get_thread_by_id(slug_or_id)

				return thread, STATUS_CODE['OK']
			except:
				message = {"message": "Can't find thread with id: " + slug_or_id}

				return message, STATUS_CODE['NOT_FOUND']
		else:
			try:
				thread = thread_repository.get_thread_by_slug(slug_or_id)

				return thread, STATUS_CODE['OK']
			except:
				message = {"message": "Can't find thread with slug: " + slug_or_id}

				return message, STATUS_CODE['NOT_FOUND']

	@staticmethod
	def update_thread(thread, new_thread):
		try:
			thread = thread_repository.update_thread(thread, new_thread)
			return thread, STATUS_CODE['OK']
		except:
			message = {"message": "Can't update thread with slug: " + thread.slug}

			return message, STATUS_CODE['CONFLICT']