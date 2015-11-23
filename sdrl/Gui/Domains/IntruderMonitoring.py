#-*- coding: utf-8 -*- 
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains import IntruderMonitoring


class IntruderMonitoringFrame( BaseFrame ):

    title = 'IntruderMonitoring'

    def __init__( self, parent=None ):
        super( IntruderMonitoringFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'IntruderMonitoringFrame.ui'))
    
    def initConfig(self):
        self.agentConfig['QLearning'] = {'lambda':0.9, 'gamma':0.9, 'alpha':0.06, 'alpha_decay_mode':'boyan', 'boyan_N0':120}
        self.agentConfig['Sarsa'] = {'lambda':0.9, 'gamma':0.9, 'alpha':0.06, 'alpha_decay_mode':'boyan', 'boyan_N0':120}
        self.policyConfig['eGreedy'] = {'epsilon':0.1}
        self.representationConfig['Tabular'] = {'discretization':50}
        self.representationConfig['iFDD'] = {'discretization':20, 'discover_threshold':1.0}
        self.representationConfig['IncrementalTabular'] = {'discretization':50}
        self.experimentConfig["maxSteps"] = 100000
        self.experimentConfig["episodeCap"] = 100
        self.experimentConfig["policyChecks"] = 10
        self.experimentConfig["checksPerPolicy"] = 1
        
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
        domain = IntruderMonitoring()

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

