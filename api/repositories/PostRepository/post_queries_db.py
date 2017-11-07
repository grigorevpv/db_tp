INSERT_POST = '''INSERT INTO posts (id, user_id, thread, forum_id, parent, created, message, path, author, forum) 
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
					RETURNING *'''

# SELECT_POST_BY_ID = '''SELECT posts.id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path
# 								FROM posts WHERE post_id = %s;'''

SELECT_POST_BY_ID = '''SELECT posts.id, posts.user_id, posts.id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent, posts.path 
								FROM posts WHERE id = %s;'''

SELECT_NEXT_VAL = '''SELECT nextval('posts_id_seq');'''

SELECT_POSTS_FLAT_SORT = '''SELECT posts.id, posts.user_id, posts.id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent, posts.path 
								FROM posts WHERE id = %s ORDER BY created %s, id %s LIMIT %s;'''

SELECT_POSTS_FLAT_SINCE_SORT = '''SELECT posts.id, posts.user_id, posts.id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent, posts.path 
								FROM posts WHERE id = %s ORDER BY created %s, id %s;'''

SELECT_POSTS_TREE_SORT = '''SELECT posts.id, posts.user_id, posts.id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent, posts.path 
								FROM posts WHERE id = %s ORDER BY path %s LIMIT %s;'''

SELECT_POSTS_TREE_SORT_SINCE = '''SELECT posts.id, posts.user_id, posts.id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent, posts.path 
								FROM posts WHERE id = %s ORDER BY path %s;'''

SELECT_COUNT_POSTS = '''SELECT count(*) as posts_count FROM posts;'''

DELETE_POSTS_TABLE = '''DELETE FROM posts;'''
