SELECT_THREADS_BY_FORUM_ID = '''SELECT threads.id, threads.forum_id, threads.user_id, 
										threads.created, threads.message, threads.slug, threads.title 
								FROM threads WHERE forum_id = %s %s ORDER BY created %s LIMIT %s;'''

COUNT_VOTES_BY_THREAD_ID = '''SELECT sum(voice) as votes_count FROM votes 
								WHERE thread_id = %s;'''

# SELECT_THREAD_BY_ID = '''SELECT threads.id, threads.forum_id, threads.user_id,
# 							threads.created, threads.message, threads.slug, threads.title
# 							FROM threads WHERE id = %s;'''

# SELECT_THREAD_BY_SLUG = '''SELECT threads.id, threads.forum_id, threads.user_id,
# 							threads.created, threads.message, threads.slug, threads.title
# 							FROM threads WHERE slug = %s;'''

SELECT_THREAD_BY_ID = '''SELECT *
							FROM threads WHERE threads.id = %s;'''

SELECT_THREAD_BY_SLUG = '''SELECT * 
							FROM threads WHERE slug = %s;'''

UPDATE_THREAD = '''UPDATE threads SET threads.message = %s, threads.title = %s
								WHERE threads.id = %s
								RETURNING threads.id, threads.forum_id, threads.user_id, 
										threads.created, threads.message, threads.slug, threads.title;'''

SELECT_COUNT_THREADS = '''SELECT count(*) as threads_count FROM threads;'''

DELETE_THREADS_TABLE = '''DELETE FROM threads;'''

SELECT_POST_BY_ID = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
								FROM posts WHERE post_id = %s;'''

ADD_THREAD = '''INSERT INTO threads (forum_id, user_id, author, created, forum, message, slug, title)
				VALUES (%s, %s, '%s', '%s', '%s', '%s', '%s', '%s')	
				RETURNING id, author, created, forum, message, slug, title;'''

