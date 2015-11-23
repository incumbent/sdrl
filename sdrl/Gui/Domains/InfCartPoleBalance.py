#-*- coding: utf-8 -*- 
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains import InfCartPoleBalance


class InfCartPoleBalanceFrame( BaseFrame ):

    title = 'InfCartPoleBalance'

    def __init__( self, parent=None ):
        super( InfCartPoleBalanceFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'InfCartPoleBalanceFrame.ui'))
    
    def initConfig(self):
        domain=InfCartPoleBalance()
        kernel_width = (domain.statespace_limits[:, 1] - domain.statespace_limits[:, 0]) \
                       / 45.016
        self.agentConfig['QLearning'] = {'lambda':0.6596, 'gamma':0.9, 'alpha':0.993, 'alpha_decay_mode':'boyan', 'boyan_N0':235}
        self.agentConfig['Sarsa'] = {'lambda':0.6596, 'gamma':0.9, 'alpha':0.993, 'alpha_decay_mode':'boyan', 'boyan_N0':235}
        self.policyConfig['eGreedy'] = {'epsilon':0.1}
        self.representationConfig['Tabular'] = {'discretization':6}
        self.representationConfig['IncrementalTabular'] = {'discretization':6}
        self.representationConfig['RBF'] = {'num_rbfs':206, 'resolution_max':25, 'resolution_min':25}
        self.representationConfig['iFDD'] = {'discretization':6, 'discover_threshold':0.037282}
        self.representationConfig['KernelizediFDD']={'sparsify':1,'kernel':gaussian_kernel,
                                                     'kernel_args':[kernel_width],
                                                     'active_threshold':0.01,
                                                     'discover_threshold':0.01356,
                                                     'max_active_base_feat':10,
                                                     'max_base_feat_sim':0.5,
                                                     'kernel_resolution':45.016}
        
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
        domain = InfCartPoleBalance()

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

