#-*- coding: utf-8 -*- 
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains import HIVTreatment


class HIVTreatmentFrame( BaseFrame ):

    title = 'HIVTreatment'

    def __init__( self, parent=None ):
        super( HIVTreatmentFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'HIVTreatmentFrame.ui'))
    
    def initConfig(self):
        domain = HIVTreatment()
        kernel_resolution=14.7920
        kernel_width = (domain.statespace_limits[:, 1] - domain.statespace_limits[:, 0]) \
                       / kernel_resolution
        self.agentConfig['QLearning'] = {'lambda':0.9, 'gamma':0.9, 'alpha':0.08, 'alpha_decay_mode':'boyan', 'boyan_N0':238}
        self.agentConfig['Sarsa'] = {'lambda':0.9, 'gamma':0.9, 'alpha':0.08, 'alpha_decay_mode':'boyan', 'boyan_N0':238}
        self.policyConfig['eGreedy'] = {'epsilon':0.1}
        self.representationConfig['IndependentDiscretization'] = {'discretization':9}
        self.representationConfig['RBF'] = {'num_rbfs':9019, 'resolution_max':13, 'resolution_min':13}
        self.representationConfig['IncrementalTabular'] = {'discretization':35}
        self.representationConfig['KernelizediFDD']={'sparsify':1,'kernel':gaussian_kernel,
                                                     'kernel_args':[kernel_width],
                                                     'active_threshold':0.01,
                                                     'discover_threshold':611850.81,
                                                     'max_active_base_feat':10,
                                                     'max_base_feat_sim':0.5,
                                                     'kernel_resolution':14.7920}
        self.representationConfig['iFDD'] = {'discretization':18, 'discover_threshold':107091}
        self.experimentConfig["maxSteps"] = 150000
        self.experimentConfig["episodeCap"] = 200
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
        domain=HIVTreatment()

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

