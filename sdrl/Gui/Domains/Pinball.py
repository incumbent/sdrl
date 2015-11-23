#-*- coding: utf-8 -*- 
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains import Pinball


class PinballFrame( BaseFrame ):

    title = 'Pinball'

    def __init__( self, parent=None ):
        super( PinballFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'PinballFrame.ui'))
    
    def initConfig(self):
        domain=Pinball()
        kernel_width = (domain.statespace_limits[:, 1] - domain.statespace_limits[:, 0]) \
                       / 10.7920
        self.agentConfig['QLearning'] = {'lambda':0.9, 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.agentConfig['Sarsa'] = {'lambda':0.9, 'gamma':0.9, 'alpha':0.1, 'alpha_decay_mode':'boyan', 'boyan_N0':100}
        self.policyConfig['eGreedy'] = {'epsilon':0.1}
        self.representationConfig['Tabular'] = {'discretization':10}
        self.representationConfig['IncrementalTabular'] = {'discretization':10}
        self.representationConfig['IndependentDiscretization'] = {'discretization':10}
        self.representationConfig['KernelizediFDD']={'sparsify':10,'kernel':gaussian_kernel,
                                                     'kernel_args':[kernel_width],
                                                     'active_threshold':0.05,
                                                     'discover_threshold':0.05,
                                                     'max_active_base_feat':100,
                                                     'max_base_feat_sim':0.5,
                                                     'kernel_resolution':10.7920}
        self.representationConfig['RBF'] = {'num_rbfs':96, 'resolution_max':8, 'resolution_min':8}
        
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
        noise = self.spNoise.value()
        domain = Pinball(noise=noise)

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

