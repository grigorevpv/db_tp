
class UserModel(object):

	def __init__(self, id, nickname, about, email, fullname):
		self._id = id
		self._nickname = nickname
		self._about = about
		self._email = email
		self._fullname = fullname

	@property
	def id(self):
		return self._id

	@property
	def nickname(self):
		return self._nickname

	@property
	def about(self):
		return self._about

	@property
	def email(self):
		return self._email

	@property
	def fullname(self):
		return self._fullname

	@classmethod
	def from_tuple(cls, my_tuple):
		id, nickname, about, email, fullname = my_tuple

		user = UserModel(
			id,
			nickname,
			about,
			email,
			fullname,
		)

		return user


	@classmethod
	def from_dict(cls, my_dict):
		id, nickname, about, email, fullname = [None for _ in range(5)]

		if 'nickname' in my_dict:
			nickname = my_dict['nickname']

		if 'about' in my_dict:
			about = my_dict['about']

		if 'email' in my_dict:
			email = my_dict['email']

		if 'fullname' in my_dict:
			fullname = my_dict['fullname']

		user = UserModel(
			id,
			nickname,
			about,
			email,
			fullname,
		)

		return user

	def update_cls(self, anower_cls):
		id, nickname, about, email, fullname = [None for _ in range(5)]

		if anower_cls.nickname is not None:
			self._nickname = anower_cls.nickname

		if anower_cls.about is not None:
			self._about = anower_cls.about

		if anower_cls.email is not None:
			self._email = anower_cls.email

		if anower_cls.fullname is not None:
			self._fullname = anower_cls.fullname


