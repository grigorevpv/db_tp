import psycopg2
from api.models.forums.ForumModel import ForumModel
from api.models.threads.ThreadModel import ThreadModel
from api.repositories.connect import connectDB
from api.repositories.ThreadRepository.thread_queries_db import *

forum_model = ForumModel
thread_model = ThreadModel


class ThreadRepository(object):
	@staticmethod
	def get_thread_by_slug(thread_slug):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_THREAD_BY_SLUG, [thread_slug, ])
			thread = cursor.fetchone()
			if thread is None:
				raise Exception("threads is not exist")

			return thread_model.from_tuple(thread)
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()

	@staticmethod
	def get_thread_by_id(thread_id):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_THREAD_BY_ID, [thread_id, ])
			thread = cursor.fetchone()
			if thread is None:
				raise Exception("threads is not exist")

			return thread_model.from_tuple(thread)
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()

	@staticmethod
	def select_threads_by_forum_id(forum, params):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			command = SELECT_THREADS_BY_FORUM_ID % (forum.id, params['since'], params['order'], params['limit'])
			cursor.execute(command)
			threads = cursor.fetchall()
			if threads is None:
				raise Exception("threads is not exist")

			thread_arr = []
			for thread in threads:
				thread_arr.append(thread_model.from_tuple(thread))

			return thread_arr
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()

	@staticmethod
	def count_votes_by_thread_id(thread_id):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(COUNT_VOTES_BY_THREAD_ID, [thread_id, ])
			count_votes = cursor.fetchone()[0]

			return count_votes
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def update_thread(thread, new_thread):
		connect = connectDB()
		cursor = connect.cursor()

		message = new_thread.message
		if message is None:
			message = thread.message

		title = new_thread.title
		if title is None:
			title = thread.title
		try:
			command = '''UPDATE threads SET message = '%s', title = '%s'
							WHERE thread_id = %s RETURNING *;''' % (str(message), str(title), thread.id)
			cursor.execute(command)
			thread = cursor.fetchone()

			return thread_model.from_tuple(thread)
		except psycopg2.IntegrityError as e:
			print("This user is already exist")
			raise
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def count_threads():
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_COUNT_THREADS)
			count_threads = cursor.fetchone()[0]

			return count_threads
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def delete_threads():
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(DELETE_THREADS_TABLE)

		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()
