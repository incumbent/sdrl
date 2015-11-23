import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui import BaseFrame
from sdrl.Gui.Utils import *
from rlpy.Domains.PuddleWorld import PuddleGapWorld, PuddleWorld

class PuddleWorldFrame( BaseFrame ):

    title = 'PuddleWorld'

    def __init__( self, parent=None ):
        super( PuddleWorldFrame, self ).__init__(parent,
            uifile=os.path.join(os.path.dirname(__file__), 'PuddleWorldFrame.ui'))
    
    def initConfig(self):
        domain = PuddleWorld()
        kernel_resolution=8.567677
        kernel_width = (domain.statespace_limits[:, 1] - domain.statespace_limits[:, 0]) \
                        / kernel_resolution
        self.agentConfig['QLearning'] = {'lambda':0.52738, 'gamma':1.0, 'alpha':0.4244, 'alpha_decay_mode':'boyan', 'boyan_N0':389.56}
        self.agentConfig['Sarsa'] = {'lambda':0.52738, 'gamma':1.0, 'alpha':0.4244, 'alpha_decay_mode':'boyan', 'boyan_N0':389.56}
        self.policyConfig['eGreedy'] = {'epsilon':0.1}
        self.representationConfig['Tabular'] = {'discretization':20}
        self.representationConfig['RBF'] = {'num_rbfs':96, 'resolution_max':21, 'resolution_min':21}
        self.representationConfig['KernelizediFDD'] = {'discover_threshold':0.0807,
                                                       'active_threshold':0.01,
                                                       'max_active_base_feat':10,
                                                       'sparsify':1,
                                                       'max_base_feat_sim':0.5,
                                                       'kernel_resolution':8.567677,
                                                       'kernel_args':[kernel_width],
                                                       'kernel':gaussian_kernel
                                                       }

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
        if(str(self.lstRepresentation.currentItem().text())=='Tabular'):
            domain=PuddleGapWorld()
        else:
            domain = PuddleWorld()        
        domain.GOAL_REWARD = float(self.spGoalReward.value())
        domain.STEP_REWARD = float(self.spStepReward.value())

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

