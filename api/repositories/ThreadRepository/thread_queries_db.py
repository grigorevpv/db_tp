SELECT_THREADS_BY_FORUM_ID = '''SELECT threads.thread_id, threads.forum_id, threads.user_id, 
										threads.created, threads.message, threads.slug, threads.title 
								FROM threads WHERE forum_id = %s %s ORDER BY created %s LIMIT %s;'''

COUNT_VOTES_BY_THREAD_ID = '''SELECT sum(voice) as votes_count FROM votes 
								WHERE thread_id = %s;'''

SELECT_THREAD_BY_ID = '''SELECT threads.thread_id, threads.forum_id, threads.user_id, 
							threads.created, threads.message, threads.slug, threads.title 
							FROM threads WHERE thread_id = %s;'''

SELECT_THREAD_BY_SLUG = '''SELECT threads.thread_id, threads.forum_id, threads.user_id, 
							threads.created, threads.message, threads.slug, threads.title 
							FROM threads WHERE slug = %s;'''