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
			# command = INSERT_POST % (post.user_id, post.thread_id, post.forum_id, post.parent_id, post.created, post.message)

			cursor.execute(INSERT_POST, [post.user_id, post.thread_id, post.forum_id, post.parent_id, post.created, post.message, ])
			returning_post = cursor.fetchone()

			return post_model.from_tuple(returning_post)
		except psycopg2.IntegrityError as e:
			print("This user is already exist" + e.diag.message_primary)
			raise
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()