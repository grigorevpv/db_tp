class ThreadModel(object):

	def __init__(self, id, forum_id, user_id, created, message, slug, title):
		self._id = id
		self._forum_id = forum_id
		self._user_id = user_id
		self._created = created
		self._message = message
		self._slug = slug
		self._title = title

	@property
	def id(self):
		return self._id

	@property
	def forum_id(self):
		return self._forum_id

	@property
	def user_id(self):
		return self._user_id

	@property
	def created(self):
		return self._created

	@property
	def message(self):
		return self._message

	@property
	def slug(self):
		return self._slug

	@property
	def title(self):
		return self._title

	@classmethod
	def from_tuple(cls, my_tuple):
		id, forum_id, user_id, created, message, slug, title = my_tuple

		thread = ThreadModel(
			id,
			forum_id,
			user_id,
			created,
			message,
			slug,
			title
		)

		return thread

	@classmethod
	def from_dict(cls, my_dict):
		id, forum_id, user_id, created, message, slug, title = [None for _ in range(7)]

		if 'forum_id' in my_dict:
			forum_id = my_dict['forum_id']

		if 'user_id' in my_dict:
			user_id = my_dict['user_id']

		if 'created' in my_dict:
			created = my_dict['created']

		if 'message' in my_dict:
			message = my_dict['message']

		if 'slug' in my_dict:
			slug = my_dict['slug']

		if 'title' in my_dict:
			title = my_dict['title']

		thread = ThreadModel(
			id,
			forum_id,
			user_id,
			created,
			message,
			slug,
			title
		)

		return thread
