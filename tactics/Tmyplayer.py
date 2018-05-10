from tactic import Tactic
import time
import sys
from skills import skill_node
from math import *


from utils.config import *
from utils.geometry import *
from skills import skills_union
from skills import sKick
from skills import sKickToPoint
from skills import sGoToPoint
from skills import sGoalie
from skills import sStop
from tactic import Tactic
from skills import sGoToBall
from skills import sGoAndKick
from skills import sGoWithDribble
import enum


class Tmyplayer(Tactic):
	def __init__(self, bot_id, state, param = None):
		super(Tmyplayer, self).__init__( bot_id, state, param)
		self.bot_id = bot_id
		self.sParams = skills_union.SParam()
	def kick_to_bot(self, state, pub, reciever_bot_id = [-1]):
		min_dist = 9999999999
		bot_index = -1
		botPos = Vector2D(state.homePos[self.bot_id].x, state.homePos[self.bot_id].y)
		our_team = [x for x in xrange(6)]
		for player in our_team:
			if player == self.bot_id:
				continue
			else:
				distance = botPos.dist(Vector2D(state.homePos[player].x, state.homePos[player].y))
				if distance < min_dist:
					min_dist = distance
					bot_index = player
		bot_index = 1
		self.sParams.KickToPointP.x = state.homePos[bot_index].x
		self.sParams.KickToPointP.y = state.homePos[bot_index].y
		print("distance: ", min_dist, " bot_id: ", self.bot_id, " x: ", state.homePos[bot_index].x, " y: ", state.homePos[bot_index].y, " index: ", bot_index)
		sGoAndKick.execute(self.sParams, state, self.bot_id, pub)
		#sGoToBall.execute(self.sParams, state, self.bot_id, pub)
		#skill_node.send_command(pub, state.isteamyellow, self.bot_id, 0, 0, 0, 7, False)
		#sKickToPoint.execute(self.sParams, state, self.bot_id, pub)
	def move_with_ball(self, params, state, pub):
		botPos = Vector2D(state.homePos[self.bot_id].x, state.homePos[self.bot_id].y)
		self.sParams.GoToPointP.x = params.x
		self.sParams.GoToPointP.y = params.y
		sGoWithDribble.execute(self.sParams, state, self.bot_id, pub)
	def execute(self,  state, pub, reciever_bot_id = [-1]):
		ballPos = Vector2D(state.ballPos.x, state.ballPos.y)
		botPos = Vector2D(state.homePos[self.bot_id].x, state.homePos[self.bot_id].y)
		params = Vector2D(4500, 0)
		self.sParams.GoToPointP.x = params.x
		self.sParams.GoToPointP.y = params.y
		sKickToPoint.execute(self.sParams, state, self.bot_id, pub)
		#self.kick_to_bot(state,pub)



	def isComplete( self, state):
		pass

	def updateParams( self, state):
		pass
	