import psycopg2
from api.models.users.UserModel import UserModel
from api.repositories.connect import connectDB
from api.repositories.UserRepository.user_queries_db import *

user_model = UserModel


class UserRepository(object):
	@staticmethod
	def insert_user(user):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(INSERT_USER,  [user.nickname, user.about, user.email, user.fullname, ])
			returning_user = cursor.fetchone()

			return user_model.from_tuple(returning_user)
		except psycopg2.IntegrityError as e:
			print("This user is already exist")
			raise
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def select_user_by_nickname_or_email(user):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_USERS_BY_NICKNAME_OR_EMAIL, [user.nickname, user.email, ])
			param_name_array = ["nickname", "about", "email", "fullname"]
			users = []

			for user in cursor.fetchall():
				users.append(dict(zip(param_name_array, user[1:])))

			return users
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	# посмотреть исключения этого метода (оставить необходимые, остальные удалить)
	def select_user_by_nickname(user_nickname):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_USERS_BY_NICKNAME, [user_nickname, ])
			user = cursor.fetchone()
			if user is None:
				raise Exception("user is not exist")

			return user_model.from_tuple(user)
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()

	@staticmethod
	# посмотреть исключения этого метода (оставить необходимые, остальные удалить)
	def select_user_by_user_id(user_id):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_USER_BY_USER_ID, [user_id, ])
			user = cursor.fetchone()
			if user is None:
				raise Exception("user is not exist")

			return user_model.from_tuple(user)
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()

	@staticmethod
	def update_user_by_nickname(user):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(UPDATE_USER_BY_NICKNAME, [user.about, user.email, user.fullname, user.nickname, ])
			user = cursor.fetchone()

			return user_model.from_tuple(user)
		except psycopg2.IntegrityError as e:
			print("This user is already exist")
			raise
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	# посмотреть исключения этого метода (оставить необходимые, остальные удалить)
	def select_users_arr(forum_id, params):
		connect = connectDB()
		cursor = connect.cursor()

		if params['since'] is not None:
			if params['desc']:
				try:
					command = SELECT_USERS_SINCE_DESC % (forum_id, forum_id, params['since'], params['limit'])
					cursor.execute(command)
					users = cursor.fetchall()
					if users is None:
						raise Exception("user is not exist")

					users_arr = []
					for user in users:
						user = user_model.from_tuple(user)
						users_arr.append(user)

					return users_arr
				except psycopg2.Error as e:
					print("PostgreSQL Error: " + e.diag.message_primary)
				except Exception as e:
					print("IntegrityError")
					raise
				finally:
					cursor.close()
			else:
				try:
					command = SELECT_USERS_SINCE % (forum_id, forum_id, params['since'], params['limit'])
					cursor.execute(command)
					users = cursor.fetchall()
					if users is None:
						raise Exception("user is not exist")

					users_arr = []
					for user in users:
						user = user_model.from_tuple(user)
						users_arr.append(user)

					return users_arr
				except psycopg2.Error as e:
					print("PostgreSQL Error: " + e.diag.message_primary)
				except Exception as e:
					print("IntegrityError")
					raise
				finally:
					cursor.close()
		else:
			if params['desc']:
				try:
					command = SELECT_USERS_DESC % (forum_id, forum_id, params['limit'])
					cursor.execute(command)
					users = cursor.fetchall()
					if users is None:
						raise Exception("user is not exist")

					users_arr = []
					for user in users:
						user = user_model.from_tuple(user)
						users_arr.append(user)

					return users_arr
				except psycopg2.Error as e:
					print("PostgreSQL Error: " + e.diag.message_primary)
				except Exception as e:
					print("IntegrityError")
					raise
				finally:
					cursor.close()
			else:
				try:
					command = SELECT_USERS % (forum_id, forum_id, params['limit'])
					cursor.execute(command)
					users = cursor.fetchall()
					if users is None:
						raise Exception("user is not exist")

					users_arr = []
					for user in users:
						user = user_model.from_tuple(user)
						users_arr.append(user)

					return users_arr
				except psycopg2.Error as e:
					print("PostgreSQL Error: " + e.diag.message_primary)
				except Exception as e:
					print("IntegrityError")
					raise
				finally:
					cursor.close()




