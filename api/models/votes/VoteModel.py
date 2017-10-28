
class VoteModel(object):

	def __init__(self, id, user_id, thread_id, voice):
		self._id = id
		self._user_id = user_id
		self._thread_id = thread_id
		self._voice = voice

	@property
	def id(self):
		return self._id

	@property
	def user_id(self):
		return self._user_id

	@property
	def thread_id(self):
		return self._thread_id

	@property
	def voice(self):
		return self._voice

	@classmethod
	def from_tuple(cls, my_tuple):
		id, user_id, thread_id, voice = my_tuple

		vote = VoteModel(
			id,
			user_id,
			thread_id,
			voice,
		)

		return vote


	@classmethod
	def from_dict(cls, my_dict):
		id, user_id, thread_id, voice = [None for _ in range(4)]

		if 'user_id' in my_dict:
			user_id = my_dict['user_id']

		if 'thread_id' in my_dict:
			thread_id = my_dict['thread_id']

		if 'voice' in my_dict:
			voice = my_dict['voice']

		vote = VoteModel(
			id,
			user_id,
			thread_id,
			voice,
		)

		return vote



