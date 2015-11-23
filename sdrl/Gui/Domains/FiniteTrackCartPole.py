#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains.FiniteTrackCartPole import FiniteCartPoleBalanceOriginal, FiniteCartPoleBalanceModern

import numpy as np

'''
param_space = {
    "num_rbfs": hp.qloguniform("num_rbfs", np.log(1e1), np.log(1e4), 1),
    'resolution': hp.quniform("resolution", 3, 30, 1),
    'boyan_N0': hp.loguniform("boyan_N0", np.log(1e1), np.log(1e5)),
    'lambda_': hp.uniform("lambda_", 0., 1.),
    'initial_learn_rate': hp.loguniform("initial_learn_rate", np.log(5e-2), np.log(1))}
'''
'''
class HackedGridWorld(GridWorld):
    def showLearning(self, representation):
        super(HackedGridWorld, self).showLearning(representation)
        plt.pause(0.001)
    def showDomain(self, a):
        super(HackedGridWorld, self).showDomain(a)
        plt.pause(0.001)

'''
class FiniteTrackCartPoleFrame( BaseFrame ):

    title = 'FiniteTrackCartPole'

    def __init__( self, parent=None ):
        super( FiniteTrackCartPoleFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'FiniteTrackCartPoleFrame.ui'))
    
    def initConfig(self):
        self.agentConfig['QLearning'] = {'lambda':0., 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.agentConfig['Sarsa'] = {'lambda':0., 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.agentConfig['Greedy_GQ'] = {'lambda':0., 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.policyConfig['eGreedy'] = {'epsilon':0.1}
        self.representationConfig['Tabular'] = {'discretization':20}
        self.representationConfig['RBF'] = {'num_rbfs':4958, 'resolution_max':8, 'resolution_min':8}
        self.representationConfig['IFDD'] = {}

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
        #noise = float(self.spNoise.value())
        position1 = float(self.spPosition1.value())
        position2 = float(self.spPosition2.value())

        velocity1 = float(self.spVelocity1.value())
        velocity2 = float(self.spVelocity2.value())
        availForce1 = float(self.spAvailForce1.value())
        availForce2 = float(self.spAvailForce2.value())
        

        domain = FiniteCartPoleBalanceOriginal(good_reward=0.)

        domain.POSITION_LIMITS = [position1, position2]
  
        #: m/s - Default limits on cart velocity [per RL Community CartPole]
        domain.VELOCITY_LIMITS = [velocity1, velocity2]

         #: Newtons, N - Force values available as actions
        domain.AVAIL_FORCE = np.array([availForce1, availForce2])

        #: kilograms, kg - Mass of the pendulum arm
        domain.MASS_PEND = float(self.spMassPend.value())
        #: kilograms, kg - Mass of cart
        domain.MASS_CART = float(self.spMassCart.value())
        #: meters, m - Physical length of the pendulum, meters (note the moment-arm lies at half this distance)
        domain.LENGTH = float(self.spLength.value())
        # m - Length of moment-arm to center of mass (= half the pendulum length)
        domain.MOMENT_ARM = domain.LENGTH / 2.
        # 1/kg - Used in dynamics computations, equal to 1 / (MASS_PEND +
        # MASS_CART)
        domain._ALPHA_MASS = 1.0 / (domain.MASS_CART + domain.MASS_PEND)

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
        


