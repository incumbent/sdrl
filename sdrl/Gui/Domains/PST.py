#-*- coding: utf-8 -*- 
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains import PST


class PSTFrame( BaseFrame ):

    title = 'PST'

    def __init__( self, parent=None ):
        super( PSTFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'PSTFrame.ui'))
    
    def initConfig(self):
        self.agentConfig['QLearning'] = {'lambda':0., 'gamma':0.9, 'alpha':0.62267772, 'alpha_decay_mode':'boyan', 'boyan_N0':3571.6541}
        self.agentConfig['Sarsa'] = {'lambda':0., 'gamma':0.9, 'alpha':0.62267772, 'alpha_decay_mode':'boyan', 'boyan_N0':3571.6541}
        self.agentConfig['Greedy_GQ'] = {'lambda':0., 'gamma':0.9, 'alpha':0.965830, 'alpha_decay_mode':'boyan', 'boyan_N0':3019.313}
        self.policyConfig['eGreedy'] = {'epsilon':0.1}
        self.representationConfig['Tabular'] = {'discretization':20}
        self.representationConfig['IndependentDiscretization'] = {'discretization':20}
        self.representationConfig['iFDD'] = {'discretization':20, 'discover_threshold':1204}
        self.experimentConfig["maxSteps"] = 500000
        self.experimentConfig["episodeCap"] = 1000
        self.experimentConfig["policyChecks"] = 30
        self.experimentConfig["checksPerPolicy"] = 10
        
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
        NUM_UAV = int(self.spNum.value())
        domain = PST(NUM_UAV=NUM_UAV)

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

