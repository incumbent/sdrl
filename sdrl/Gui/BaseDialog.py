#-*- coding: utf-8 -*-
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic

class BaseDialog( QDialog ):

    # 仅可放置SpinBox
    configSpinBoxes = None

    def __init__( self, parent, config, uifile ):
        self.config = config
        super( BaseDialog, self ).__init__(parent)
        uic.loadUi( uifile, self )
    
    def accept(self):
        self.saveConfig()
        self.close()

    def applyConfig(self):
        for name in self.configSpinBoxes:
            if name in self.config:
                self.configSpinBoxes[name].setValue(self.config[name])

    def saveConfig(self):
        for name in self.configSpinBoxes:
            self.config[name] = self.configSpinBoxes[name].value()