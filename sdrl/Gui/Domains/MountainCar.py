#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains import MountainCar

from rlpy.Experiments import Experiment

import numpy as np

class MountainCarFrame( BaseFrame ):

    title = 'MountainCar'

    def __init__(self, parent=None):
        super( MountainCarFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'MountainCarFrame.ui'))	

    def initConfig(self):
        self.agentConfig['QLearning'] = {'lambda':0., 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.agentConfig['Sarsa'] = {'lambda':0., 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.policyConfig['eGreedy'] = {'epsilon':0.2}
        self.representationConfig['Tabular'] = {'discretization':20}
        self.representationConfig['RBF'] = {"num_rbfs":206}
        self.representationConfig['TilingCoding'] = {}

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
        
        #Define a Domain of MountainCar
        noise = float(self.dblSpinVelNoise.value())
        domain = MountainCar(noise=noise)

        domain.XMIN = float(self.dblSpinleftPos.value())  # : Lower bound on domain position
        domain.XMAX = float(self.dblSpinRightPos.value())  #: Upper bound on domain position
        domain.XDOTMIN = float(self.dblSpinMinVelocity.value())  # : Lower bound on car velocity
        domain.XDOTMAX = float(self.dblSpinMaxVelocity.value())  #: Upper bound on car velocity
        domain.INIT_STATE = np.array([float(self.dblSpinInitPos.value()), float(self.dblSpinInitVelocity.value())])  # : Initial car state
        #: X-Position of the goal location (Should be at/near hill peak)
        domain.GOAL = float(self.dblSpinGoal.value())


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
