#-*- coding: utf-8 -*-
import os
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
from sdrl.Gui.Utils import DialogMapping

class BaseFrame( QFrame ):

    title = None

    def __init__( self, parent, uifile ):
        self.agentConfig = {}
        self.representationConfig = {}
        self.policyConfig = {}
        super( BaseFrame, self ).__init__(parent)
        uic.loadUi( uifile, self )
        self.initConfig()

    def loadDialogByName(self, name, config):
        # 每个项目(name)有自己的子config
        if not name in config:
            config[name] = {}
            
        dialogClass = None
        if name in DialogMapping:
            dialogClass = DialogMapping[name]
            if dialogClass == None:
                return None
        else:
            raise Exception('Cannot find config dialog for ' + name + ', check DialogMapping')

        return dialogClass(self, config[name])

    def showDialogByName(self, name, config):
        dialog = self.loadDialogByName(name, config)
        if dialog == None:
            QMessageBox.information(None, u'提示', name+u'没有参数可以设置', QMessageBox.Ok)
            return
        dialog.setWindowTitle(name+u'设置')
        dialog.setModal(True)
        dialog.show()
    
    '''
    abstract method
    初始化各参数（设默认值）
    '''
    def initConfig(self):
        pass
    
    '''
    abstract method
    根据参数生成domain和agent
    returns (domain, agent)
    '''
    def makeComponents(self):
        pass