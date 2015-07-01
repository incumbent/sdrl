#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from sdrl.Gui import BaseDialog

class eGreedyDialog( BaseDialog ):

    def __init__( self, parent, config ):
        super( eGreedyDialog, self ).__init__(parent, config,
            uifile=os.path.join(os.path.dirname(__file__), 'eGreedyDialog.ui'))
        self.configSpinBoxes = {'epsilon':self.spEpsilon}
        self.applyConfig()
