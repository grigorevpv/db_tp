import psycopg2
from api.models.forums.ForumModel import ForumModel
from api.models.threads.ThreadModel import ThreadModel
from api.repositories.connect import connectDB
from api.repositories.ThreadRepository.thread_queries_db import *

forum_model = ForumModel
thread_model = ThreadModel


class ThreadRepository(object):
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
