import psycopg2
from api.models.users.UserModel import UserModel
from api.repositories.UserRepository.connect import connectDB
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
	def select_user(user):
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

