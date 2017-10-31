from api.repositories.VoteRepository.VoteRepository import VoteRepository
from api.repositories.ForumRepository.ForumRepository import ForumRepository
from api.repositories.UserRepository.UserRepository import UserRepository
from api.repositories.ThreadRepository.ThreadRepository import ThreadRepository
from api.models.votes.VoteModel import VoteModel
from enquiry.secondary import *

vote_repository = VoteRepository()
user_repository = UserRepository()
forum_repository = ForumRepository()
thread_repository = ThreadRepository()
vote_model = VoteModel

STATUS_CODE = {
	'OK': 200,
	'CREATED': 201,
	'NOT_FOUND': 404,
	'CONFLICT': 409
}


class VoteService(object):

	@staticmethod
	def create_vote(thread, user, vote):
		try:
			user = user_repository.select_user_by_nickname(user.nickname)
		except:
			message = {"message": "Can't find user with nickname: " + user.nickname}

			return thread, user,message, STATUS_CODE['NOT_FOUND']
		try:
			exist_vote = vote_repository.select_vote(thread.id, user.id)
			if exist_vote.voice != vote.voice:
				exist_vote = vote_repository.update_vote(vote.voice, thread.id, user.id)

			return thread, user, exist_vote, STATUS_CODE['OK']
		except:
			try:
				vote_content = dict()
				vote_content['user_id'] = user.id
				vote_content['thread_id'] = thread.id
				vote_content['voice'] = vote.voice
				vote = vote_model.from_dict(vote_content)

				vote = vote_repository.insert_vote(vote)

				return thread, user, vote, STATUS_CODE['OK']
			except:
				message = {"message": "Can't create vote, it's exist "}

				return thread, user, message, STATUS_CODE['CONFLICT']

	@staticmethod
	def count_votes_by_thread_id(thread_id):
		try:
			count_votes = vote_repository.count_votes_by_thread_id(thread_id)

			return count_votes, STATUS_CODE['OK']
		except:
			message = {"message": "Can't create thread with id: " + thread_id}

			return message, STATUS_CODE['NOT_FOUND']

	@staticmethod
	def count_votes():

		try:
			message_or_count = vote_repository.count_votes()
		except:
			message = {"message": "Votes is not exist"}

			return message, STATUS_CODE['NOT_FOUND']



