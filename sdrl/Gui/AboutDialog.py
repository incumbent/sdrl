#-*- coding: utf-8 -*-
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
import os

class AboutDialog( QDialog ):

    def __init__( self, parent ):
        super( AboutDialog, self ).__init__(parent)
        uic.loadUi( os.path.join(os.path.dirname(__file__), 'AboutDialog.ui'), self )
        self.setFixedSize(self.width(), self.height())
    