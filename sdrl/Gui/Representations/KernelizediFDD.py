#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from sdrl.Gui import BaseDialog

class KernelizediFDDDialog( BaseDialog ):

    def __init__( self, parent, config ):
        super( KernelizediFDDDialog, self ).__init__(parent, config,
            uifile=os.path.join(os.path.dirname(__file__), 'KernelizediFDDDialog.ui'))
        self.configSpinBoxes = {'sparsify':self.spSparsify,
                                'kernel_resolution':self.spKernelResolution,
                                'active_threshold':self.spActiveThreshold,
                                'discover_threshold':self.spDiscoverThreshold,
                                'max_active_base_feat':self.spMaxActiveBaseFeat,
                                'max_base_feat_sim':self.spMaxBaseFeatSim
                                }
        self.applyConfig()
