class PostModel(object):

	def __init__(self, id, user_id, thread_id, forum_id, created, isedited, message, parent_id):
		self._id = id
		self._user_id = user_id
		self._thread_id = thread_id
		self._forum_id = forum_id
		self._created = created
		self._isedited = isedited
		self._message = message
		self._parent_id = parent_id

	@property
	def id(self):
		return self._id

	@property
	def user_id(self):
		return self._user_id

	@property
	def thread_id(self):
		return self._thread_id

	@property
	def forum_id(self):
		return self._forum_id

	@property
	def created(self):
		return self._created

	@property
	def isedited(self):
		return self._isedited

	@property
	def message(self):
		return self._message

	@property
	def parent_id(self):
		return self._parent_id

	@classmethod
	def from_tuple(cls, my_tuple):
		id, user_id, thread_id, forum_id, created, isedited, message, parent_id = my_tuple

		post = PostModel(
			id,
			user_id,
			thread_id,
			forum_id,
			created,
			isedited,
			message,
			parent_id
		)

		return post

	@classmethod
	def from_dict(cls, my_dict):
		id, user_id, thread_id, forum_id, created, isedited, message, parent_id = [None for _ in range(8)]

		if 'user_id' in my_dict:
			user_id = my_dict['user_id']

		if 'thread_id' in my_dict:
			thread_id = my_dict['thread_id']

		if 'forum_id' in my_dict:
			forum_id = my_dict['forum_id']

		if 'created' in my_dict:
			created = my_dict['created']

		if 'isedited' in my_dict:
			isedited = my_dict['isedited']

		if 'message' in my_dict:
			message = my_dict['message']

		if 'parent_id' in my_dict:
			parent_id = my_dict['parent_id']

		post = PostModel(
			id,
			user_id,
			thread_id,
			forum_id,
			created,
			isedited,
			message,
			parent_id
		)

		return post
