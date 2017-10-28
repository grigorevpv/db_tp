import psycopg2
from api.models.votes.VoteModel import VoteModel
from api.repositories.connect import connectDB
from api.repositories.VoteRepository.vote_queries_db import *

vote_model = VoteModel


class VoteRepository(object):
	@staticmethod
	def insert_vote(vote):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(INSERT_VOTE,  [vote.user_id, vote.thread_id, vote.voice, ])
			returning_vote = cursor.fetchone()

			return vote_model.from_tuple(returning_vote)
		except psycopg2.IntegrityError as e:
			print("This vote is already exist")
			raise
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def select_vote(thread_id, user_id):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(SELECT_VOTE_BY_THREAD_AND_USER_ID, [thread_id, user_id])
			vote = cursor.fetchone()
			if vote is None:
				raise Exception("vote is not exist")

			return vote_model.from_tuple(vote)
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError")
			raise
		finally:
			cursor.close()

	@staticmethod
	def count_votes_by_thread_id(thread_id):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(COUNT_VOTES_BY_THREAD_ID, [thread_id, ])
			count_votes = cursor.fetchone()[0]
			if count_votes is None:
				raise Exception("vote is not exist")

			return count_votes
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		except Exception as e:
			print("IntegrityError" + + e.diag.message_primary)
		finally:
			cursor.close()

	@staticmethod
	def update_vote(voice, thread_id, user_id):
		connect = connectDB()
		cursor = connect.cursor()

		try:
			cursor.execute(UPDATE_VOTE, [voice, user_id, thread_id, ])
			returning_vote = cursor.fetchone()

			return vote_model.from_tuple(returning_vote)
		except psycopg2.IntegrityError as e:
			print("This vote is already exist")
			raise
		except psycopg2.Error as e:
			print("PostgreSQL Error: " + e.diag.message_primary)
		finally:
			cursor.close()
