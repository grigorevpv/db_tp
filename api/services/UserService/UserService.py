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

	@staticmethod
	def select_users_arr(forum, params):
		limit, since, desc = 100, None, False

		if 'limit' in params:
			limit = params.get('limit')

		if 'desc' in params:
			if params.get('desc') == 'true':
				desc = True

		if 'since' in params:
			since = params.get('since')

		new_params = dict()
		new_params['limit'] = limit
		new_params['since'] = since
		new_params['desc'] = desc
		try:
			users_arr = user_repository.select_users_arr(forum.id, new_params)
			return users_arr, STATUS_CODE['OK']
		except:
			message = {"message": "Can't select users"}

			return message, STATUS_CODE['CONFLICT']

	@staticmethod
	def count_users():

		try:
			message_or_count = user_repository.count_users()
			return message_or_count, STATUS_CODE['OK']
		except:
			message = {"message": "Users is not exist"}
			return message, STATUS_CODE['NOT_FOUND']

	@staticmethod
	def delete_users():

		try:
			user_repository.delete_users()
			return STATUS_CODE['OK']
		except:
			message = {"message": "Forums is not exist"}
			return message, STATUS_CODE['NOT_FOUND']