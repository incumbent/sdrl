#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains import SystemAdministrator


class SystemAdministratorFrame( BaseFrame ):

    title = 'SystemAdministrator'

    def __init__( self, parent=None ):
        super( SystemAdministratorFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'SystemAdministratorFrame.ui'))
    
    def initConfig(self):
        self.agentConfig['QLearning'] = {'lambda':0.9, 'gamma':0.95, 'alpha':.06, 'alpha_decay_mode':'boyan', 'boyan_N0':120}
        self.agentConfig['Sarsa'] = {'lambda':0.9, 'gamma':0.95, 'alpha':.06, 'alpha_decay_mode':'boyan', 'boyan_N0':120}
        self.agentConfig['Greedy_GQ'] = {'lambda':0.9, 'gamma':0.95, 'alpha':.06, 'alpha_decay_mode':'boyan', 'boyan_N0':120}
        self.policyConfig['eGreedy'] = {'epsilon':0.1}
        self.representationConfig['Tabular'] = {'discretization':20}
        self.representationConfig['IncrementalTabular'] = {'discretization':20}
        self.representationConfig['IndependentDiscretization'] = {'discretization':20}
        self.experimentConfig['episodeCap'] = 200
        self.experimentConfig["maxSteps"] = 100000
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
        map_type = str(self.lstMap.currentItem().text())
        domain = SystemAdministrator(networkmapname=os.path.join(
                SystemAdministrator.default_map_dir, map_type+'.txt'))
        domain.P_SELF_REPAIR = float(self.spSelfRepairProb.value())
        domain.P_REBOOT_REPAIR = float(self.spRobotRepairProb.value())
        domain.REBOOT_REWARD = float(self.spRobotReward.value())

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

