from api.repositories.UserRepository.UserRepository import UserRepository

user_repository = UserRepository()

STATUS_CODE = {
	'OK': 200,
	'CREATED': 201,
	'NOT_FOUND': 404,
	'CONFLICT': 409
}


class UserService(object):

	@staticmethod
	def create_user(user):
		try:
			user = user_repository.insert_user(user)
		except:
			user = user_repository.select_user_by_nickname_or_email(user)

			return user, STATUS_CODE['CONFLICT']

		return user, STATUS_CODE['CREATED']

	@staticmethod
	def select_user_by_nickname(user_nickname):
		try:
			user = user_repository.select_user_by_nickname(user_nickname)
		except:
			message = {"message": "Can't find user with nickname =" + user_nickname}

			return message, STATUS_CODE['NOT_FOUND']

		return user, STATUS_CODE['OK']

	@staticmethod
	def select_user_by_user_id(user_id):
		try:
			user = user_repository.select_user_by_user_id(user_id)
		except:
			message = {"message": "Can't find user with id =" + user_id}

			return message, STATUS_CODE['NOT_FOUND']

		return user, STATUS_CODE['OK']

	@staticmethod
	def update_user_by_nickname(user):
		try:
			user = user_repository.update_user_by_nickname(user)
		except:
			message = {"message": "New user's data have been conflicted with existing"}

			return message, STATUS_CODE['CONFLICT']

		return user, STATUS_CODE['OK']
