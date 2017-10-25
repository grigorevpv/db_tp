import psycopg2
from api.models.forums.ForumModel import ForumModel
from api.models.threads.ThreadModel import ThreadModel
from api.repositories.connect import connectDB
from api.repositories.PostRepository.post_queries_db import *

forum_model = ForumModel
thread_model = ThreadModel


class PostRepository(object):
	@staticmethod
	def create_post(post):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(INSERT_POST,  [post.user_id, post.thread_id, post.forum_id, post.created,
											post.message, post.parent_id])
			returning_post = cursor.fetchone()

			return forum_model.from_tuple(returning_post)
		except psycopg2.IntegrityError as e:
			print("This user is already exist" + e.diag.message_primary)
			raise
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()