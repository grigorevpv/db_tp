import psycopg2
from api.models.forums.ForumModel import ForumModel
from api.models.threads.ThreadModel import ThreadModel
from api.repositories.connect import connectDB
from api.repositories.ForumRepository.forum_queries_db import *

forum_model = ForumModel
thread_model = ThreadModel


class ForumRepository(object):
	@staticmethod
	def create_forum(forum, user):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(INSERT_FORUM,  [user.id, forum.slug, forum.title, ])
			returning_forum = cursor.fetchone()

			return forum_model.from_tuple(returning_forum)
		except psycopg2.IntegrityError as e:
			print("This user is already exist" + e.diag.message_primary)
			raise
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def count_posts_by_forum_id(forum):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_COUNT_POSTS_BY_FORUM_ID, [forum.id, ])
			count_posts = cursor.fetchone()[0]

			return count_posts
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def count_threads_by_forum_id(forum):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_COUNT_THREADS_BY_FORUM_ID, [forum.id, ])
			count_threads = cursor.fetchone()[0]

			return count_threads
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def select_forum_by_slug(forum_slug):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_FORUM_BY_SLUG, [forum_slug, ])
			forum = cursor.fetchone()
			if forum is None:
				raise Exception("forum is not exist")

			return forum_model.from_tuple(forum)
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()

	@staticmethod
	def select_forum_by_id(forum_id):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_FORUM_BY_ID, [forum_id, ])
			forum = cursor.fetchone()
			if forum is None:
				raise Exception("forum is not exist")

			return forum_model.from_tuple(forum)
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()

	@staticmethod
	def create_thread(thread, forum, user):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(INSERT_THREAD, [forum.id, user.id, thread.created, thread.message, thread.slug, thread.title, ])
			returning_thread = cursor.fetchone()

			return thread_model.from_tuple(returning_thread)
		except psycopg2.IntegrityError as e:
			print("This user is already exist" + e.diag.message_primary)
			raise
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def count_forums():
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_COUNT_FORUMS)
			count_forums = cursor.fetchone()[0]

			return count_forums
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def delete_forums():
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(DELETE_FORUMS_TABLE)

		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()
