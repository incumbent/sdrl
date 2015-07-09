#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains import GridWorld


class GridWorldFrame( BaseFrame ):

    title = 'GridWorld'

    def __init__( self, parent=None ):
        super( GridWorldFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'GridWorldFrame.ui'))
    
    def initConfig(self):
        self.agentConfig['QLearning'] = {'lambda':0., 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.agentConfig['Sarsa'] = {'lambda':0., 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.agentConfig['Greedy_GQ'] = {'lambda':0., 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.policyConfig['eGreedy'] = {'epsilon':0.2}
        self.representationConfig['Tabular'] = {'discretization':20}
        self.representationConfig['IncrementalTabular'] = {'discretization':20}
        self.representationConfig['IndependentDiscretization'] = {'discretization':20}

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
        map_type = str(self.lstMap.currentItem().text())
        noise = self.spNoise.value()
        maze = os.path.join(GridWorld.default_map_dir, map_type+'.txt')
        domain = GridWorld(maze, noise=noise)
        domain.GOAL_REWARD = self.spGoalReward.value()
        domain.PIT_REWARD = self.spPitReward.value()
        domain.STEP_REWARD = self.spStepReward.value()

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

