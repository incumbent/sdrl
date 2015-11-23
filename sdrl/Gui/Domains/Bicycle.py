#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains import BicycleBalancing, BicycleRiding

class BicycleFrame( BaseFrame ):

    title = 'Bicycle'

    def __init__(self, parent=None):
        super( BicycleFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'BicycleFrame.ui'))	

    def initConfig(self):
        domain=BicycleBalancing()
        kernel_resolution=11.6543336229
        kernel_width = (domain.statespace_limits[:, 1] - domain.statespace_limits[:, 0]) \
                       / kernel_resolution
        self.agentConfig['QLearning'] = {'lambda':0.43982644088, 'gamma':0.98, 'alpha':0.920244401, 'alpha_decay_mode':'boyan', 'boyan_N0':1885.42}
        self.agentConfig['Sarsa'] = {'lambda':0.43982644088, 'gamma':0.98, 'alpha':0.920244401, 'alpha_decay_mode':'boyan', 'boyan_N0':1885.42}
        self.representationConfig['KernelizediFDD']={'sparsify':1,'kernel':gaussian_kernel,
                                                     'kernel_args':[kernel_width],
                                                     'active_threshold':0.01,
                                                     'discover_threshold':88044,
                                                     'max_active_base_feat':10,
                                                     'max_base_feat_sim':0.5,
                                                     'kernel_resolution':11.6543336229}
        self.policyConfig['SwimmerPolicy']={'epsilon':0.1}
        self.policyConfig['eGreedy'] = {'epsilon':0.1}
        self.experimentConfig["maxSteps"] = 150000
        self.experimentConfig["episodeCap"] = 50000
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
        map_type = str(self.lstMap.currentItem().text())
        
        if (map_type=='BicycleRiding') :
            domain=BicycleRiding()
        elif (map_type=='BicycleBalancing') :
            domain=BicycleBalancing()
            
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
