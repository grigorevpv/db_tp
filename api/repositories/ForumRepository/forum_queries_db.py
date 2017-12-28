SELECT_FORUM_BY_SLUG = '''SELECT forums.forum_id, forums.user_id, forums.slug, forums.title 
							FROM forums WHERE slug = %s;'''

SELECT_FORUM_BY_ID = '''SELECT forums.forum_id, forums.user_id, forums.posts, forums.slug, forums.threads, forums.title, forums.user 
								FROM forums WHERE forum_id = %s;'''

INSERT_FORUM = '''INSERT INTO forums (user_id, slug, title, "user")
					VALUES (%s, %s, %s, %s) 
					RETURNING forums.forum_id, forums.user_id, forums.posts, forums.slug, forums.threads, forums.title, forums.user;'''

# INSERT_THREAD = '''INSERT INTO threads (forum_id, user_id, author, created, forum, message, slug, title)
# 					VALUES (%s, %s, '%s', '%s', '%s', '%s', '%s', '%s')
# 					RETURNING threads.thread_id, threads.forum_id, threads.user_id, threads.author, threads.created, threads.forum,
# 								threads.message, threads.slug, threads.title, threads.votes;'''

INSERT_THREAD = '''INSERT INTO threads (forum_id, user_id, author, created, forum, message, slug, title) 
					VALUES (%s, %s, '%s', '%s', '%s', '%s', '%s', '%s')	RETURNING *;'''

SELECT_COUNT_POSTS_BY_FORUM_ID = '''SELECT count(*) as posts_count FROM posts 
										WHERE forum_id = %s;'''

SELECT_COUNT_THREADS_BY_FORUM_ID = '''SELECT count(*) as threads_count FROM threads 
										WHERE forum_id = %s;'''

SELECT_COUNT_FORUMS = '''SELECT count(*) as forums_count FROM forums;'''

DELETE_FORUMS_TABLE = '''DELETE FROM forums;'''

INCREMENT_THREADS = '''UPDATE forums SET threads = threads + 1 WHERE forums.forum_id = %s;'''

INCREMENT_POSTS = '''UPDATE forums SET posts = posts + 1 WHERE forums.forum_id = %s;'''

INCREMENT_POSTS_BY_NUMBER = "UPDATE forums SET posts = posts + %s WHERE forums.forum_id = %s;"
