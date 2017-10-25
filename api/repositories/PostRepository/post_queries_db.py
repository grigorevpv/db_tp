INSERT_POST = """INSERT INTO posts (user_id, thread_id, forum_id, created, message, parent_id) 
					VALUES %s, %s, %s, %s, %s, %s
					RETURNING posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, 
					posts.created, posts.isedited, posts.message, posts.parent_id"""
