#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains import Pacman


class PacmanFrame( BaseFrame ):

    title = 'Pacman'

    def __init__( self, parent=None ):
        super( PacmanFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'PacmanFrame.ui'))
    
    def initConfig(self):
        self.agentConfig['QLearning'] = {'lambda':0.9, 'gamma':0.9, 'alpha':0.068, 'alpha_decay_mode':'boyan', 'boyan_N0':22.36}
        self.agentConfig['Sarsa'] = {'lambda':0.9, 'gamma':0.9, 'alpha':0.068, 'alpha_decay_mode':'boyan', 'boyan_N0':22.36}
        self.policyConfig['eGreedy'] = {'epsilon':0.1}
        self.representationConfig['IncrementalTabular'] = {'discretization':9}
        self.experimentConfig["maxSteps"] = 150000
        self.experimentConfig["policyChecks"] = 30
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
        domain = Pacman()

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

