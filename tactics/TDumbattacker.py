from tactic import Tactic
import time
import sys
from math import *
from utils.config import *
import enum

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
from skills import sTurnToPoint


import numpy as np
from numpy import array,inf
from isPossible import isPossible

k1 = True
K2 = True

class TDumbattacker(Tactic):
    def __init__(self, bot_id, state, param=None):
        super(TDumbattacker, self).__init__( bot_id, state, param)
        self.sParams = skills_union.SParam()
        self.bot_id = bot_id
        self.receive_bot_id = -1
        self.passer_bot_id = -1
        self.GOAL_UPPER = Vector2D(HALF_FIELD_MAXX,OUR_GOAL_MAXY*3)
        self.GOAL_LOWER = Vector2D(HALF_FIELD_MAXX,OUR_GOAL_MINY*3)
 

    class State(enum.Enum):
        #shoot towards goal 
        shoot = 1
        #cross pass
        cross_pass = 2
        #cross receive
        cross_receive = 3
        #dribble before passing or shooting
        optimum_pos = 4

    def getState(self,state):
        botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))
        ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        goal_angle_upper = atan((self.GOAL_UPPER.y-botPos.y)*1.0/ (self.GOAL_UPPER.x-botPos.x))
        goal_angle_lower = atan((self.GOAL_LOWER.y-botPos.y)*1.0/ (self.GOAL_LOWER.x-botPos.x))
        goal_angle_mid   = 0.5*(goal_angle_lower+goal_angle_upper)

        global k1
        global k2
        for away_bot in xrange(len(state.awayPos)):
            
            if state.awayPos[away_bot].x > state.homePos[self.bot_id].x:
                ##print (state.awayPos[away_bot].x, state.homePos[self.bot_id].x, "chutiya.....")
                away_BOT = Vector2D (int(state.awayPos[away_bot].x), int(state.awayPos[away_bot].y))
                try:
                    bot_angle = atan((away_BOT.y - botPos.y)*1.0/ (away_BOT.x - botPos.x))
                except:
                    bot_angle = fabs((away_BOT.y - botPos.y))

                ##print("bhosdiwala angles ",bot_angle, goal_angle_lower, goal_angle_mid, goal_angle_upper, away_bot)
                if bot_angle > goal_angle_lower and bot_angle < goal_angle_mid:
                    k1=False
                     
                if bot_angle > goal_angle_mid and bot_angle < goal_angle_upper:
                    k2=False
                #print(k1,k2)
        for home_bot in xrange(len(state.homePos)):
            if home_bot == state.our_goalie:
                continue
            
            if state.homePos[home_bot].x > state.homePos[self.bot_id].x:
                ##print (state.homePos[home_bot].x, state.homePos[self.bot_id].x, "chutiya.....")
                home_BOT = Vector2D (int(state.homePos[home_bot].x), int(state.homePos[home_bot].y))
                try:
                    bot_angle = atan((home_BOT.y - botPos.y)*1.0/ (home_BOT.x - botPos.x))
                except:
                    bot_angle = fabs((home_BOT.y - botPos.y))

                ##print("bhosdiwala angles ",bot_angle, goal_angle_lower, goal_angle_mid, goal_angle_upper, home_bot)
                if bot_angle > goal_angle_lower and bot_angle < goal_angle_mid:
                    k1=False
                     
                if bot_angle > goal_angle_mid and bot_angle < goal_angle_upper:
                    k2=False
        
        if k1 or k2 :
            return TDumbattacker.State.shoot

        ball_in_possession = False
        pass_possible = True
        for home_bot in xrange(len(state.homePos)):
            if fabs(ballPos.dist(Vector2D(int(state.homePos[home_bot].x),int(state.homePos[home_bot].y)))<BOT_BALL_THRESH):
                ball_in_possession = True
                self.passer_bot_id = home_bot
                break   
    
        for home_bot in xrange(len(state.homePos)):
            if state.homePos[home_bot].x > state.homePos[passer_bot_id]:
                angle = State.homePos[passer_bot_id].angle(State.homePos[home_bot])
                for awayBot in xrange(len(state.awayPos)):
                    if fabs(State.homePos[passer_bot_id].angle(State.homePos[away_bot]) - angle) < 0.15:
                        pass_possible = False
                if pass_possible == True:
                    receive_bot_id = home_bot
                    break

        if ball_in_possession :
            return TDumbattacker.State.cross_pass

        if fabs(ballPos.dist(Vector2D(int(state.homePos[self.bot_id].x),int(state.homePos[self.bot_id].y)))>1200 and ball_in_possession and pass_possible):
            return TDumbattacker.State.cross_receive

        if fabs(ballPos.dist(Vector2D(int(state.homePos[self.bot_id].x),int(state.homePos[self.bot_id].y)))>1200 and ball_in_possession and not pass_possible):
            return TDumbattacker.State.optimum_pos 

    def execute(self, state , pub):
        print "BALL_POS : ",state.ballPos.x,",",state.ballPos.y
        ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))
        ballVel = Vector2D(int(state.ballVel.x) , int(state.ballVel.y))
        gameState = self.getState(state)
        global k1
        global k2

        if gameState == TDumbattacker.State.shoot:
            if not (state.ballPos.x < -HALF_FIELD_MAXX + DBOX_WIDTH ) :
                if fabs(ballPos.dist(Vector2D(int(state.homePos[self.bot_id].x),int(state.homePos[self.bot_id].y)))>BOT_BALL_THRESH):
                    sGoToBall.execute(self.sParams, state, self.bot_id, pub)
            else:
                return

            if k1 and not k2 :
                self.sParams.KickToPointP.x = HALF_FIELD_MAXX      
                self.sParams.KickToPointP.y = 0.8*OUR_GOAL_MINY
                self.sParams.KickToPointP.power = 10
                sKickToPoint.execute(self.sParams, state, self.bot_id, pub)
            else:
                self.sParams.KickToPointP.x = HALF_FIELD_MAXX      
                self.sParams.KickToPointP.y = 0.8*OUR_GOAL_MAXY
                self.sParams.KickToPointP.power = 10
                sKickToPoint.execute(self.sParams, state, self.bot_id, pub)

        if gameState == TDumbattacker.State.cross_pass:
            self.sParams.KickToPointP.x = state.homePos[self.receive_bot_id].x
            self.sParams.KickToPointP.y = state.homePos[self.receive_bot_id].y
            self.sParams.KickToPointP.power = 7
            sKickToPoint.execute(self.sParams,state,self.bot_id,pub)

        if gameState == TDumbattacker.State.cross_receive:
            self.SParams.sTurnToPoint.x = state.homePos[self.passer_bot_id].x
            self.SParams.sTurnToPoint.y = state.homePos[self.passer_bot_id].y
            self.SParams.sTurnToPoint.max_omega = MAX_BOT_OMEGA
            sTurnToPoint.execute(self.sParams,state,self.bot_id,pub)

        if gameState == TDumbattacker.State.optimum_pos:
            if state.homePos[self.passer_bot_id].y > 0 :
                if state.homePos[self.bot_id].x < state.homePos[self.passer_bot_id].x :
                    self.SParams.sGoToPoint.y = OUR_GOAL_MAXY*1.5
                    self.SParams.sGoToPoint.x = state.homePos[self.passer_bot_id].x + 100
                    self.SParams.sGoToPoint.finalSlope = -State.homePos[self.bot_id].angle(State.homePos[self.passer_bot_id])
                    self.SParams.sGoToPoint.align = False
                    self.SParams.sGoToPoint.finalVelocity = 0
                    sGoToPoint.execute(self.sParams,state,self.bot_id,pub)
                else :
                    self.SParams.sGoToPoint.y = OUR_GOAL_MAXY*1.5
                    self.SParams.sGoToPoint.x = self.SParams.sGoToPoint.x + 75
                    self.SParams.sGoToPoint.finalSlope = -State.homePos[self.bot_id].angle(State.homePos[self.passer_bot_id])
                    self.SParams.sGoToPoint.align = False
                    self.SParams.sGoToPoint.finalVelocity = 0
            else:
                if state.homePos[self.bot_id].x < state.homePos[self.passer_bot_id].x :
                    self.SParams.sGoToPoint.y = OUR_GOAL_MINY*1.5
                    self.SParams.sGoToPoint.x = state.homePos[self.passer_bot_id].x + 100
                    self.SParams.sGoToPoint.finalSlope = -State.homePos[self.bot_id].angle(State.homePos[self.passer_bot_id])
                    self.SParams.sGoToPoint.align = False
                    self.SParams.sGoToPoint.finalVelocity = 0
                    sGoToPoint.execute(self.sParams,state,self.bot_id,pub)
                else :
                    self.SParams.sGoToPoint.y = OUR_GOAL_MINY*1.5
                    self.SParams.sGoToPoint.x = self.SParams.sGoToPoint.x + 75
                    self.SParams.sGoToPoint.finalSlope = -State.homePos[self.bot_id].angle(State.homePos[self.passer_bot_id])
                    self.SParams.sGoToPoint.align = False
                    self.SParams.sGoToPoint.finalVelocity = 0


    def isComplete(self,state):
    	pass
    def updateParams(self,state):
    	pass







