from api.repositories.UserRepository.UserRepository import UserRepository

user_repository = UserRepository()

STATUS_CODE = {
	'OK': 200,
	'CREATED': 201,
	'NOT_FOUND': 400,
	'CONFLICT': 409
}


class UserService(object):

	@staticmethod
	def create_user(user):
		try:
			user = user_repository.insert_user(user)
		except:
			user = user_repository.select_user(user)
			return user, STATUS_CODE['CONFLICT']

		return user, STATUS_CODE['CREATED']
