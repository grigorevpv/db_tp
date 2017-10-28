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
	def posts_flat_sort_sql(thread, params):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_POSTS_FLAT_SORT, [thread.id, params['order'], params['order'], params['limit'] ])
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



def posts_flat_sort_since_sql(slug_or_id, desc):
    sql = "SELECT author, created, forum, id, isEdited, message, parent, thread FROM posts WHERE thread = "
    if slug_or_id.isdigit():
        sql += "%(slug_or_id)s"
    else:
        sql += "(SELECT id FROM threads WHERE slug = %(slug_or_id)s)"
    sql += " ORDER BY created"
    if desc:
        sql += " DESC"
    sql += ", id"
    if desc:
        sql += " DESC"
    return sql

def posts_tree_sort_sql(slug_or_id, desc):
    sql = "SELECT author, created, forum, id, isEdited, message, parent, thread FROM posts WHERE thread = "
    if slug_or_id.isdigit():
        sql += "%(slug_or_id)s"
    else:
        sql += "(SELECT id FROM threads WHERE slug = %(slug_or_id)s)"
    sql += " ORDER BY path"
    if desc:
        sql += " DESC"
    sql += " LIMIT %(limit)s"
    return sql

def posts_tree_sort_since_sql(slug_or_id, desc):
    sql = "SELECT author, created, forum, id, isEdited, message, parent, thread FROM posts WHERE thread = "
    if slug_or_id.isdigit():
        sql += "%(slug_or_id)s"
    else:
        sql += "(SELECT id FROM threads WHERE slug = %(slug_or_id)s)"
    sql += " ORDER BY path"
    if desc:
        sql += " DESC"
    return sql


def posts_parent_tree_sort_sql(slug_or_id, desc):
    sql = """SELECT author, created, forum, id, isEdited, message, parent, thread 
				FROM posts 
				WHERE root_id IN (
					SELECT id
					FROM posts
					WHERE thread = """
    if slug_or_id.isdigit():
        sql += "%(slug_or_id)s"
    else:
        sql += "(SELECT id FROM threads WHERE slug = %(slug_or_id)s)"
    sql += " AND parent = 0 ORDER BY id"
    if desc:
        sql += " DESC"
    sql += " LIMIT %(limit)s OFFSET %(since)s)"
    sql += " ORDER BY path"
    if desc:
        sql += " DESC"
    return sql

def posts_parent_tree_sort_since_sql(slug_or_id, desc):
    sql = """SELECT author, created, forum, id, isEdited, message, parent, thread 
				FROM posts 
				WHERE root_id IN (
					SELECT id
					FROM posts
					WHERE thread = """
    if slug_or_id.isdigit():
        sql += "%(slug_or_id)s"
    else:
        sql += "(SELECT id FROM threads WHERE slug = %(slug_or_id)s)"
    sql += " AND parent = 0 ORDER BY id"
    if desc:
        sql += " DESC"

    sql += ") ORDER BY path"
    if desc:
        sql += " DESC"
    return sql


def posts_since_limit_parent (content, since, limit):
    for i in range(len(content) - 1):
        if content[i]["id"] == since:
            start = i + 1
            stop = start
            flag = 1
            for j in range (start, len(content)-1):
                if content[j]["parent"] == "0":
                    flag += 1
                if flag > limit:
                    break
                stop += 1
            return content[start:stop+2]
    return []

def posts_since_limit (content, since, limit):
    for i in range(len(content) - 1):
        if content[i]["id"] == since:
            return content[i+1:i+limit+1]
    return []

