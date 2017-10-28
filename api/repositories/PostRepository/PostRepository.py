import psycopg2
from api.models.forums.ForumModel import ForumModel
from api.models.threads.ThreadModel import ThreadModel
from api.models.posts.PostModel import PostModel
from api.repositories.connect import connectDB
from api.repositories.PostRepository.post_queries_db import *

forum_model = ForumModel
thread_model = ThreadModel
post_model = PostModel


class PostRepository(object):
	@staticmethod
	def create_post(post):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_NEXT_VAL)
			post_id = cursor.fetchone()[0]
			post_path = post.path
			post_path = post_path.append(post_id)
			cursor.execute(INSERT_POST, [post_id, post.user_id, post.thread_id, post.forum_id, post.parent_id, post.created, post.message, post.path ])
			returning_post = cursor.fetchone()

			return post_model.from_tuple(returning_post)
		except psycopg2.IntegrityError as e:
			print("This user is already exist" + e.diag.message_primary)
			raise
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def select_post_by_id(post_id):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_POST_BY_ID, [post_id, ])
			post = cursor.fetchone()
			if post is None:
				raise Exception("post is not exist")

			return post_model.from_tuple(post)
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()

	@staticmethod
	def posts_flat_sort(thread, params):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			command = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
							FROM posts WHERE thread_id = %s ORDER BY created %s, post_id %s LIMIT %s;''' % (thread.id, params['order'], params['order'], params['limit'])
			cursor.execute(command)
			posts = cursor.fetchall()
			if posts is None:
				raise Exception("post is not exist")

			post_arr = []
			for post in posts:
				post_arr.append(post_model.from_tuple(post))

			return post_arr
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()


	@staticmethod
	def posts_flat_sort_since(thread, params):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_POSTS_FLAT_SINCE_SORT, [thread.id, params['order'], params['order'], ])
			posts = cursor.fetchall()
			if posts is None:
				raise Exception("post is not exist")

			post_arr = []
			for post in posts:
				post_arr.append(post_model.from_tuple(post))

			return post_arr
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()

	@staticmethod
	def posts_tree_sort(thread, params):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			command = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
										FROM posts WHERE thread_id = %s ORDER BY path %s, post_id %s LIMIT %s;''' % (thread.id, params['order'], params['order'], params['limit'])
			cursor.execute(command)
			posts = cursor.fetchall()
			if posts is None:
				raise Exception("post is not exist")

			post_arr = []
			for post in posts:
				post_arr.append(post_model.from_tuple(post))

			return post_arr
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()

	@staticmethod
	def posts_tree_sort_since(thread, params):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_POSTS_TREE_SORT, [thread.id, params['order'], ])
			posts = cursor.fetchall()
			if posts is None:
				raise Exception("post is not exist")

			post_arr = []
			for post in posts:
				post_arr.append(post_model.from_tuple(post))

			return post_arr
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()

	@staticmethod
	def posts_parent_tree_sort(thread, params):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			command = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, 
								posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
								FROM posts WHERE path[1] IN (SELECT posts.post_id FROM posts 
								WHERE thread_id = %s AND parent_id = 0 ORDER BY post_id %s 
								LIMIT %s OFFSET %s) ORDER BY path %s;''' % (thread.id, params['order'], params['limit'], params['since'], params['order'])
			cursor.execute(command)
			posts = cursor.fetchall()
			if posts is None:
				raise Exception("post is not exist")

			post_arr = []
			for post in posts:
				post_arr.append(post_model.from_tuple(post))

			return post_arr
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()






