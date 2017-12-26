import psycopg2
from api.models.forums.ForumModel import ForumModel
from api.models.threads.ThreadModel import ThreadModel
from api.models.posts.PostModel import PostModel
from api.repositories.connect import connectDB
from api.repositories.PostRepository.post_queries_db import *

forum_model = ForumModel
thread_model = ThreadModel
post_model = PostModel


def posts_since_limit(content, since, limit):
    for i in range(len(content) - 1):
        if content[i][0] == int(since):
            return content[i+1:i+int(limit)+1]
    return []


def posts_since_limit_parent(content, since, limit):
    for i in range(len(content) - 1):
        if content[i][0] == int(since):
            start = i + 1
            stop = start
            flag = 1
            for j in range(start, len(content)-1):
                if content[j][7] == 0:
                    flag += 1
                if flag > int(limit):
                    break
                stop += 1
            return content[start:stop+2]
    return []


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
			command = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
								FROM posts WHERE thread_id = %s ORDER BY created %s, post_id %s;''' % (thread.id, params['order'], params['order'])
			cursor.execute(command)
			posts = cursor.fetchall()
			if posts is None:
				raise Exception("post is not exist")

			posts = posts_since_limit(posts, params['since'], params['limit'])
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
			command = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
								FROM posts WHERE thread_id = %s ORDER BY path %s;''' % (thread.id, params['order'])
			cursor.execute(command)
			posts = cursor.fetchall()
			if posts is None:
				raise Exception("post is not exist")

			posts = posts_since_limit(posts, params['since'], params['limit'])
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

	@staticmethod
	def posts_parent_tree_sort_since(thread, params):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			command = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, 
									posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
									FROM posts WHERE path[1] IN (SELECT posts.post_id FROM posts 
									WHERE thread_id = %s AND parent_id = 0 ORDER BY post_id %s) 
									ORDER BY path %s;''' % (thread.id, params['order'], params['order'])
			cursor.execute(command)
			posts = cursor.fetchall()
			if posts is None:
				raise Exception("post is not exist")

			posts = posts_since_limit_parent(posts, params['since'], params['limit'])
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
	def update_post(post, message):
		connect = connectDB()
		cursor = connect.cursor()
		isEdited = True

		try:
			command = '''UPDATE posts SET message = '%s', isedited = %s
								WHERE post_id = %s RETURNING *;''' % (message, isEdited, post.id)
			cursor.execute(command)
			post = cursor.fetchone()

			return post_model.from_tuple(post)
		except psycopg2.IntegrityError as e:
			print("This user is already exist")
			raise
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def count_posts():
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_COUNT_POSTS)
			count_posts = cursor.fetchone()[0]

			return count_posts
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def delete_posts():
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(DELETE_POSTS_TABLE)

		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()





