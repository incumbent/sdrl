#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from sdrl.Gui import BaseDialog

class RBFDialog( BaseDialog ):

    def __init__( self, parent, config ):
        super( RBFDialog, self ).__init__(parent, config,
            uifile=os.path.join(os.path.dirname(__file__), 'RBFDialog.ui'))
        self.configSpinBoxes = {'num_rbfs':self.spNumRbfs}
        self.applyConfig()
