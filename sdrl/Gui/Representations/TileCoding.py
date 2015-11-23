#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from sdrl.Gui import BaseDialog

class TileCodingDialog( BaseDialog ):

    def __init__( self, parent, config ):
        super( TileCodingDialog, self ).__init__(parent, config,
            uifile=os.path.join(os.path.dirname(__file__), 'TileCodingDialog.ui'))
        self.configSpinBoxes = {'memory':self.spMemory,
                                'num_tilings':self.spNum_tilings}
        self.applyConfig()
