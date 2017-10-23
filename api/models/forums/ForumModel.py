
class ForumModel(object):

	def __init__(self, id, user_id, slug, title):
		self._id = id
		self._user_id = user_id
		self._slug = slug
		self._title = title

	@property
	def id(self):
		return self._id

	@property
	def user_id(self):
		return self._user_id

	@property
	def slug(self):
		return self._slug

	@property
	def title(self):
		return self._title

	@classmethod
	def from_tuple(cls, my_tuple):
		id, user_id, slug, title = my_tuple

		forum = ForumModel(
			id,
			user_id,
			slug,
			title,
		)

		return forum

	@classmethod
	def from_dict(cls, my_dict):
		id, user_id, slug, title = [None for _ in range(4)]

		if 'id' in my_dict:
			id = my_dict['id']

		if 'user_id' in my_dict:
			user_id = my_dict['user_id']

		if 'slug' in my_dict:
			slug = my_dict['slug']

		if 'title' in my_dict:
			fullname = my_dict['title']

		forum = ForumModel(
			id,
			user_id,
			slug,
			title,
		)

		return forum

