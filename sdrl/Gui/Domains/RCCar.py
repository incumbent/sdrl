#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains import RCCar
import matplotlib.pyplot as plt


class RCCarFrame( BaseFrame ):

    title = 'RCCar'

    def __init__( self, parent=None ):
        super( RCCarFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'RCCarFrame.ui'))
    
    def initConfig(self):
        self.agentConfig['QLearning'] = {'lambda':0., 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.agentConfig['Sarsa'] = {'lambda':0., 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.agentConfig['Greedy_GQ'] = {'lambda':0., 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.policyConfig['eGreedy'] = {'epsilon':0.2}
        self.representationConfig['Tabular'] = {'discretization':10}
        self.representationConfig['RBF'] = {'num_rbfs':600, 'resolution_max':8, 'resolution_min':8}
        self.representationConfig['iFDD'] = {'discretization':20}

    @pyqtSlot()
    def on_btnConfigAgent_clicked(self):
        self.showDialogByName( str(self.lstAgent.currentItem().text()), self.agentConfig )

    @pyqtSlot()
    def on_btnConfigRepresentation_clicked(self):
        self.showDialogByName( str(self.lstRepresentation.currentItem().text()), self.representationConfig )

    @pyqtSlot()
    def on_btnConfigPolicy_clicked(self):
        self.showDialogByName( str(self.lstPolicy.currentItem().text()), self.policyConfig )


    def makeComponents(self):
        noise = float(self.spNoise.value())
        domain = RCCar( noise=noise )       
        domain.GOAL = [float(self.spGoal_X.value()),float(self.spGoal_Y.value())]
        domain.GOAL_RADIUS = float(self.spGoalRadius.value())
        domain.ROOM_WIDTH = float(self.spRoomWidth.value())
        domain.ROOM_HEIGHT = float(self.spRoomHeight.value())        
        domain.GOAL_REWARD = float(self.spGoalReward.value())        
        domain.STEP_REWARD = float(self.spStepReward.value())
        domain.CAR_LENGTH = float(self.spCarLength.value())
        domain.CAR_WIDTH = float(self.spCarWidth.value())
        domain.delta_t = float(self.spDeltaT.value())
        
        representation = RepresentationFactory.get(config=self.representationConfig,
            name=str(self.lstRepresentation.currentItem().text()),
            domain=domain)

        policy = PolicyFactory.get(config=self.policyConfig,
            name=str(self.lstPolicy.currentItem().text()),
            representation=representation)

        agent = AgentFactory.get(config=self.agentConfig,
            name=str(self.lstAgent.currentItem().text()),
            representation=representation,
            policy=policy)

        return domain, agent

