from api.repositories.ForumRepository.ForumRepository import ForumRepository
from api.repositories.UserRepository.UserRepository import UserRepository
from api.repositories.PostRepository.PostRepository import PostRepository

user_repository = UserRepository()
forum_repository = ForumRepository()
post_repository = PostRepository()

STATUS_CODE = {
	'OK': 200,
	'CREATED': 201,
	'NOT_FOUND': 404,
	'CONFLICT': 409
}


class PostService(object):

	@staticmethod
	def create_post(post):
		try:
			post_parent = post_repository.select_post_by_id(post.parent_id)
			path = list()
			# for num in post_parent.path:
			# 	path.append(num)
			path.extend(post_parent.path)
			post.path = path
		except:
			print("post parent is not exist")
		try:
			post = post_repository.create_post(post)

			return post, STATUS_CODE['CREATED']
		except:
			message = {"message": "Post didn't created"}

			return message, STATUS_CODE['CONFLICT']

	@staticmethod
	def select_post_by_id(post_id):
		try:
			post = post_repository.select_post_by_id(post_id)

			return post, STATUS_CODE['OK']
		except:
			message = {"message": "Didn't find post with id: " + post_id}

			return message, STATUS_CODE['NOT_FOUND']

	@staticmethod
	def get_posts_arr(thread, params):
		limit = ' ALL '
		if 'limit' in params:
			limit = params.get('limit')
		order = 'asc'
		if 'desc' in params:
			order = 'desc' if params.get('desc') == 'true' else 'asc'
		since = 0
		if 'since' in params:
			since = params.get('since')
		sort = 'flat'
		if 'sort' in params:
			sort = params.get('sort')
		order = ' ' + order + ' '

		new_params = dict()
		new_params['limit'] = limit
		new_params['order'] = order
		new_params['sort'] = sort
		new_params['since'] = since

		message = {"message": "Error in sorting posts"}

		if sort == 'flat':
			if since == 0:
				try:
					posts_arr = post_repository.posts_flat_sort(thread, new_params)
					return posts_arr, STATUS_CODE['OK']
				except:
					return message, STATUS_CODE['CONFLICT']
			else:
				try:
					posts_arr = post_repository.posts_flat_sort_since(thread, new_params)
					return posts_arr, STATUS_CODE['OK']
				except:
					print("[PostService] get_posts_arr flat sort with since error")
					return message, STATUS_CODE['CONFLICT']
		elif sort == 'tree':
			if since == 0:
				try:
					posts_arr = post_repository.posts_tree_sort(thread, new_params)
					return posts_arr, STATUS_CODE['OK']
				except:
					print("[PostService] get_posts_arr tree sort error")
					return message, STATUS_CODE['CONFLICT']
			else:
				try:
					posts_arr = post_repository.posts_tree_sort_since(thread, new_params)
					return posts_arr, STATUS_CODE['OK']
				except:
					print("[PostService] get_posts_arr tree sort with since error")
					return message, STATUS_CODE['CONFLICT']
		elif sort == 'parent_tree':
			if since == 0:
				try:
					posts_arr = post_repository.posts_parent_tree_sort(thread, new_params)
					return posts_arr, STATUS_CODE['OK']
				except:
					print("[PostService] get_posts_arr parent_tre sort error")
					return message, STATUS_CODE['CONFLICT']
			else:
				try:
					posts_arr = post_repository.posts_parent_tree_sort_since(thread, new_params)
					return posts_arr, STATUS_CODE['OK']
				except:
					print("[PostService] get_posts_arr parent_tre sort with since error")
					return message, STATUS_CODE['CONFLICT']

	@staticmethod
	def update_post(post, message):
		try:
			post = post_repository.update_post(post, message)
			return post, STATUS_CODE['OK']
		except:
			message = {"message": "Can't update post with id: " + post.id}

			return message, STATUS_CODE['CONFLICT']

	@staticmethod
	def count_posts():

		try:
			message_or_count = post_repository.count_posts()
			return message_or_count, STATUS_CODE['OK']
		except:
			message = {"message": "Posts is not exist"}
			return message, STATUS_CODE['NOT_FOUND']

	@staticmethod
	def delete_posts():

		try:
			post_repository.delete_posts()
			return STATUS_CODE['OK']
		except:
			message = {"message": "Posts is not exist"}
			return message, STATUS_CODE['NOT_FOUND']