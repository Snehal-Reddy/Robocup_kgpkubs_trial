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
import enum


class TPass(Tactic):
	def __init__(self, bot_id, state, param = None):
		super(TPass, self).__init__( bot_id, state, param)
		self.bot_id = bot_id
		self.sParams = skills_union.SParam()

	class State(enum.Enum):
		#Danger of conceeding a goal so kick the ball in safe place
		throw_away = 1
		#If in a position to score then score
		into_the_goal = 2
		#free_kick
		free_kick = 4
		#penalty_kick
		penalty_kick = 5
		#normal pass
		normal_pass = 6
		# execute normal pass
		chill = 7



	def find_channels(self, state):
		botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[botPos].y))
		angle = state.homePos[self.bot_id].theta
		opp_bots = [x for x in xrange(6)]
		team = [x for x in xrange(6)]
		bot_occ_ang = []
		for opp in opp_bots:
			ang_pos = atan2(1.0*(state.awayPos[opp].y-state.homePos[self.bot_id].y), 1.0*(state.awayPos[opp].x-state.homePos[self.bot_id].x))
			dis_from_opp = botPos.dist(Vector2D(int(state.awayPos[opp].x), int(state.homePos[opp].y)))
			ang_thresh = fabs(asin(BOT_RADIUS/dis_from_opp))
			bot_occ_ang.append([ang_pos-ang_thresh, ang_pos+ang_thresh, opp])
		bot_occ_ang.sort( key = lambda x:x[0])
		open_angles = []
		for i in xrangle(len(bot_occ_ang)):
			j = i+1
			if i == len(bot_occ_angle):
				continue
			else:
				b1 = bot_occ_ang[i][2]
				b2 = bot_occ_ang[j][2]
				#d1 = botPos.dist(Vector2D(int(state.awayPos[b1].x), int(state.awayPos[b1].y)))
				#d2 = botPos.dist(Vector2D(int(state.awayPos[b2].x), int(state.awayPos[b2].y)))
				open_angles.append([bot_occ_ang[i][1], bot_occ_ang[j][0], b1, b2])
		for players in team:
			player_ang_pos = atan2(1.0*(state.homePos[players].y-state.homePos[self.bot_id].y), 1.0*(state.homePos[players].x-state.homePos[players].x))
			player_dist = botPos.dist(Vector2D(int(state.homePos[players].x), int(state.homePos[players].y)))
			for angles in open_angles:
				if player_ang_pos > angles[0] and player_ang_pos < angles[1]:
					angles.append(players)
					break
				else:
					continue
		return open_angles

	def diaganose(self, state, bot_id, channels):
		ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
		opp_team = [x for x in xrange(6)]
		botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))
		opp_in_our_Dbox = 0
		opp_too_much_inside = 0
		opp_in_inner_half = 0
		opp_in_outer_half = 0
		remaining = 0
		for opp in opp_team:
			if state.awayPos[opp].x < -HALF_FIELD_MAXX+D_BOX_HEIGHT and state.awayPos[opp].x > -HALF_FIELD_MAXX:
				if state.awayPos[opp].y < D_BOX_WIDTH and state.awayPos[opp].y > -D_BOX_WIDTH:
					opp_in_our_Dbox += 1
				else :
					opp_too_much_inside += 1
			elif state.awayPos[opp].x < -0.5*( HALF_FIELD_MAXX-D_BOX_HEIGHT):
				opp_in_inner_half += 1
			elif state.awayPos[opp].x < 0:
				opp_in_outer_half += 1
			else:
				remaining += 1
		if opp_in_our_Dbox >= 2:
			return TPass.State.throw_away
		elif opp_in_inner_half >= 3:
			return TPass.State.throw_away
		elif opp_in_our_Dbox == 1:
			if opp_in_inner_half >= 2:
				return TPass.State.throw_away
			else:
				return TPass.State.chill
		elif opp_in_our_Dbox == 0:
			if opp_in_inner_half + opp_in_outer_half == 3:
				return TPass.State.throw_away
			else:
				return TPass.State.chill
		else:
			pass


	def execute(self, state, pub, reciever_bot_id = [-1]):
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

	def isComplete( self, state):
		pass

	def updateParams( self, state):
		pass
	


		# ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
		# botPos = Vector2D(int(state.homePos[]))
		# all_team = [x for x in xrange(6)]
		# channels = find_channels(self, state)
		# min_dist = 999999999
		# bot_index = -1
		# for player in all_team:
		# 	if player == 0:
		# 		continue
		# 	dist = botPos.dist(Vector2D(int(state.homePos[player]), int(state.homePos[player])))
		# 	if min_dist < dist:
		# 		min_dist = dist
		# 		bot_index = player
		# self.sParams.KickToPointP.x = state.homePos[channels[0][4]].x
		# self.sParams.KickToPointP.y = state.homePos[channels[0][4]].y
		# sKickToPoint.execute(self.sParams, state, 0, pub)


		# channels = find_channels(self, state)
		# min_dist = 999999999
		# bot_index = -1
		# if len(channels) == 0:
		# 	all_team = [x for x in xrange(6)]
		# 	for player in all_team:
		# 		dist = botPos.dist(Vector2D(int(state.homePos[player]), int(state.homePos[player])))
		# 		if min_dist < dist:
		# 			min_dist = dist
		# 			bot_index = player

		
