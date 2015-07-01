#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from sdrl.Gui import BaseDialog

'''
通用Agent设置窗口
适用于继承了(Agent, DescentAlgorithm)的Agent
具有参数: alpha, gamma, lambda, alpha衰减方式, boyan_N0
'''
class CommonAgentDialog( BaseDialog ):

    def __init__( self, parent, config ):
        super( CommonAgentDialog, self ).__init__(parent, config,
            uifile=os.path.join(os.path.dirname(__file__), 'CommonAgentDialog.ui'))
        self.configSpinBoxes = {'lambda':self.spLambda,
                                'gamma':self.spGamma,
                                'alpha':self.spAlpha,
                                'boyan_N0':self.spBoyanN0}
        self.applyConfig()

    def applyConfig(self):
        super( CommonAgentDialog, self ).applyConfig()
        index = self.cbAlphaDecay.findText(self.config['alpha_decay_mode'])
        self.cbAlphaDecay.setCurrentIndex(index)

    def saveConfig(self):
        super( CommonAgentDialog, self ).saveConfig()
        self.config['alpha_decay_mode'] = str(self.cbAlphaDecay.currentText())