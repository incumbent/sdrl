#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from sdrl.Gui import BaseDialog

class iFDDDialog( BaseDialog ):

    def __init__( self, parent, config ):
        super( iFDDDialog, self ).__init__(parent, config,
            uifile=os.path.join(os.path.dirname(__file__), 'iFDDDialog.ui'))
        self.configSpinBoxes = {'discretization':self.spDiscretization,
        						'discover_threshold':self.spDiscover_threshold}
        self.applyConfig()