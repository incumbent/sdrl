#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains import BlocksWorld

class BlocksWorldFrame( BaseFrame ):

    title = 'BlocksWorld'
    block_number = None
    def __init__( self, parent=None ):
        super( BlocksWorldFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'BlocksWorldFrame.ui'))
    
    def initConfig(self):
        self.agentConfig['QLearning'] = {'lambda':0., 'gamma':0.9, 'alpha':.6102,'alpha_decay_mode':'boyan', 'boyan_N0':10.25}
        self.agentConfig['Sarsa'] = {'lambda':0., 'gamma':0.9, 'alpha':.6102,'alpha_decay_mode':'boyan', 'boyan_N0':10.25}
        self.agentConfig['Greedy_GQ'] = {'lambda':0., 'gamma':0.9, 'alpha':.6102,'alpha_decay_mode':'boyan', 'boyan_N0':10.25}
        self.representationConfig['Tabular'] = {'discretization':20}
        self.representationConfig['iFDD'] = {'discretization':20, 'discover_threshold':0.031049}
        self.representationConfig['IndependentDiscretization'] = {'discretization':20}
        self.representationConfig['TileCoding'] = {'memory':2000, 'num_tilings':2}
        self.policyConfig['eGreedy'] = {'epsilon':0.1}

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
        self.block_number = int(self.spinBoxBlocksNumber.value())
        noise = float(self.spNoise.value())
        domain = BlocksWorld(blocks=self.block_number,towerSize=self.block_number, noise=noise)
        domain.GOAL_REWARD = float(self.spGoalReward.value())
        domain.STEP_REWARD = float(self.spStepReward.value())

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

