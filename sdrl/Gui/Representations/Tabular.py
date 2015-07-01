#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from sdrl.Gui import BaseDialog

class TabularDialog( BaseDialog ):

    def __init__( self, parent, config ):
        super( TabularDialog, self ).__init__(parent, config,
            uifile=os.path.join(os.path.dirname(__file__), 'TabularDialog.ui'))
        self.configSpinBoxes = {'discretization':self.spDiscretization}
        self.applyConfig()