import skill_node
import math 
import sys

from utils.config import *
from utils.geometry import *
from navigation_py.wrapperpy import *
from navigation_py.obstacle import Obstacle

import skills_union
import sGoToBall
import sGoToPoint
import sTurnToPoint
import sKickToPoint

flag1 = 0
flag2 = 0

def execute(param, state, bot_id, pub):
	global flag1, flag2
	botPos = Vector2D(param.KickToPointP.x, param.KickToPointP.y)
	currbotPos = Vector2D(state.homePos[bot_id].x, state.homePos[bot_id].y)
	ballPos = Vector2D(state.ballPos.x, state.ballPos.y)
	#point = Vector2D()
	distance = ballPos.dist(botPos)
	dis_bn_ball_bot = ballPos.dist(currbotPos)
	req_dis =	BOT_BALL_THRESH-10
	angle = botPos.angle(ballPos)
	ang = ballPos.angle(currbotPos)
	par = skills_union.SParam()
	par.GoToPointP.x = ballPos.x + req_dis*math.cos(angle)
	par.GoToPointP.y = ballPos.y + req_dis*math.sin(angle)
	par.GoToPointP.finalSlope = ballPos.angle(botPos)
	par.GoToPointP.align = True
	par.GoToPointP.finalVelocity = 0
	# par.GoToBallP.intercept = False

	sGoToPoint.execute(par, state, bot_id, pub)

	par1 = skills_union.SParam()
	par1.KickToPointP.x = botPos.x
	par1.KickToPointP.y = botPos.y
	par1.KickToPointP.power = 7

	sKickToPoint.execute(par1, state, bot_id, pub)
	return

	# targetPos = Vector2D(par.GoToPointP.x, par.GoToPointP.y)
	# print "distance : ", dis_bn_ball_bot
	# print "thresh: ", BOT_BALL_THRESH
	# sGoToPoint.execute(par, state, bot_id, pub)
	# print " check :", ballPos.dist(currbotPos)
	# if ballPos.dist(currbotPos) < BOT_BALL_THRESH+30:
	# 	sKickToPoint.execute(par1, state, bot_id, pub)
	# 	return
	# return
	# if targetPos.dist(currbotPos) > 150:
	# 	print "err : ", targetPos.dist(currbotPos)
	# 	sGoToPoint.execute(par, state, bot_id, pub)
	# 	print "no1 - ", state.frame_number
	# 	return


	# par1 = skills_union.SParam()
	# par1.KickToPointP.x = botPos.x
	# par1.KickToPointP.y = botPos.y
	# par1.KickToPointP.power = 7
	# #par1.TurnToPointP.MAX_BOT_OMEGA = 50

	# sKickToPoint.execute(par1, state, bot_id, pub)
	# return
	#sTurnToPoint.execute(par1, state, bot_id, pub)
	
	#par1.TurnToPointP.max_omega = MAX_BOT_OMEGA
	# if currbotPos.dist(targetPos) < 10:
	# 	print "1"
	# 	flag1 = 1


	
	# diff = math.fabs(math.fabs(state.homePos[bot_id].theta) - math.fabs(angle))*180.0/math.pi
	# if currbotPos.dist(targetPos) < 100000 :#and ( math.fabs(diff-180) > 5 ):
	# 	print "2"
	# 	#diff = math.fabs(math.fabs(state.homePos[bot_id].theta) - math.fabs(angle))*180.0/math.pi
	# 	print " a: ", diff
	# 	print "no2 - ", state.frame_number
	# 	sKickToPoint.execute(par1, state, bot_id, pub)
	# 	#sTurnToPoint.execute(par1, state, bot_id, pub)
	# 	return 
	
	# par.GoToPointP.x = ballPos.x + 100*math.cos(angle)
	# par.GoToPointP.x = ballPos.x + 100*math.cos(angle)
	# sGoToPoint.execute(par, state, bot_id, pub)
	# if math.fabs(math.fabs(state.homePos[bot_id].theta) - math.fabs(ang))*180.0/math.pi < 5:
	# 	print "3"
	# 	flag2 = 1
	
	
	# o = Vector2D()
	# diff = math.fabs(math.fabs(state.homePos[bot_id].theta) - math.fabs(angle))*180.0/math.pi
	# print("ang: ", math.fabs(math.fabs(o.normalizeAngle(state.homePos[bot_id].theta)) - math.fabs(o.normalizeAngle(ang)))*180.0/math.pi )
	# if currbotPos.dist(targetPos) < 100:
	# 	print( "a1: ", math.fabs(math.fabs(state.homePos[bot_id].theta) - math.fabs(ang))*180.0/math.pi )
	# 	if math.fabs(math.fabs(state.homePos[bot_id].theta) - math.fabs(ang))*180.0/math.pi < 5:
	# 		print "4"
	# 		sGoToBall.execute(param, state, bot_id, pub)
	# 		return 
	

	# if currbotPos.dist(targetPos) < 100:
	# 	print( "a2: ", (math.fabs(state.homePos[bot_id].theta) - math.fabs(ang))*180.0/math.pi -90)
	# 	if math.fabs((math.fabs(state.homePos[bot_id].theta) - math.fabs(ang))*180.0/math.pi -90) < 5:
	# 		print "4"
	# 		sGoToBall.execute(param, state, bot_id, pub)
	# 		return
	# print("distance1: ", distance)
	# print("distance: ", dis1)
	

	# if dis1 < 150 and currbotPos.dist(targetPos) < 10 and math.fabs(math.fabs(state.homePos[bot_id].theta) - math.fabs(ang))*180.0/math.pi < 5:
	# 	print "5"
	# 	print("distance: ", dis1)
	# 	skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, 0, 7, False)
	# 	return


