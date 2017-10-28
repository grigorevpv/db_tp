INSERT_POST = '''INSERT INTO posts (post_id, user_id, thread_id, forum_id, parent_id, created, message, path) 
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
					RETURNING posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path;'''

SELECT_POST_BY_ID = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
								FROM posts WHERE post_id = %s;'''

SELECT_NEXT_VAL = '''SELECT nextval('posts_post_id_seq');'''

SELECT_POSTS_FLAT_SORT = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
								FROM posts WHERE thread_id = %s ORDER BY created %s, post_id %s LIMIT %s;'''

SELECT_POSTS_FLAT_SINCE_SORT = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
								FROM posts WHERE thread_id = %s ORDER BY created %s, post_id %s;'''

SELECT_POSTS_TREE_SORT = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
								FROM posts WHERE thread_id = %s ORDER BY path %s LIMIT %s;'''

SELECT_POSTS_TREE_SORT_SINCE = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
								FROM posts WHERE thread_id = %s ORDER BY path %s;'''