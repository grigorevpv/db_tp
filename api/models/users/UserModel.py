
class UserModel(object):

	def __init__(self, id, nickname, about, email, fullname):
		self._id = id
		self._nickname = nickname
		self._about = about
		self._email = email
		self._fullname = fullname

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

