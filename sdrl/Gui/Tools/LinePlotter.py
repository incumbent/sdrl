﻿#-*- coding: utf-8 -*-
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic
import matplotlib
matplotlib.rcdefaults()

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import numpy as np
from StringIO import StringIO
import os
import sys
import pickle

class LinePlotterWindow( QMainWindow ):

    def __init__( self, parent=None ):
        super( LinePlotterWindow, self ).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        uic.loadUi( os.path.join(os.path.dirname(__file__), 'LinePlotterWindow.ui'), self )
        self.config = {}
        fig = Figure()
        self.axes = fig.add_subplot(111)
        self.canvas = FigureCanvas(fig)
        self.mplLayout.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, 
                self.mplWidget, coordinates=True)
        self.mplLayout.addWidget(self.toolbar)

    def saveConfig(self, filename):
        self.collectConfigs()
        fp = open(filename, 'wb')
        pickle.dump(self.config, fp)
        fp.close()

    def loadConfig(self, filename):
        fp = open(filename, 'rb')
        self.config = pickle.load(fp)
        fp.close()
        self.applyConfig(self.config)

    def applyConfig(self, config):
        self.txtTitle.setText(config['title'])
        self.txtXLabel.setText(config['xlabel'])
        self.txtYLabel.setText(config['ylabel'])
        self.spXlim0.setValue(config['xlim'][0])
        self.spXlim1.setValue(config['xlim'][1])
        self.spYlim0.setValue(config['ylim'][0])
        self.spYlim1.setValue(config['ylim'][1])
        self.chkShowLegend.setChecked(config['showLegend'])

    def collectConfigs(self):
        self.config['xlim'] = [self.spXlim0.value(), self.spXlim1.value()]
        self.config['ylim'] = [self.spYlim0.value(), self.spYlim1.value()]
        self.config['title'] = self.txtTitle.text()
        self.config['xlabel'] = self.txtXLabel.text()
        self.config['ylabel'] = self.txtYLabel.text()
        self.config['showLegend'] = self.chkShowLegend.isChecked()
        
    @pyqtSlot()
    def on_actionSave_triggered(self):
        fn = QFileDialog.getSaveFileName(self, filter=u'配置文件 (*.sdplt)')
        if fn != u'':
            self.saveConfig(fn)

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        fn = QFileDialog.getOpenFileName(self, filter=u'配置文件 (*.sdplt)')
        if fn != u'':
            self.loadConfig(fn)
            self.on_btnPlot_clicked()

    @pyqtSlot()
    def on_actionExit_triggered(self):
        self.close()

    @pyqtSlot()
    def on_actionLoadExample_triggered(self):
        self.loadConfig(os.path.join(os.path.dirname(__file__), 'example.sdplt'))
        self.on_btnPlot_clicked()

    @pyqtSlot()
    def on_btnEditData_clicked(self):
        if not 'data' in self.config:
            self.config['data'] = []
        f = LinePlotterDataEditor(self, self.config['data'])
        f.setModal(True)
        f.show()

    @pyqtSlot()
    def on_btnPlot_clicked(self):
        self.collectConfigs()

        ax = self.axes
        ax.cla()

        for d in self.config['data']:
            dd = d['ydata']
            ax.plot(dd, **d)

        if self.config['xlim'][0] != 0 or self.config['xlim'][1] != 0:
            ax.set_xlim(self.config['xlim'])
        if self.config['ylim'][0] != 0 or self.config['ylim'][1] != 0:
            ax.set_ylim(self.config['ylim'])
        
        ax.set_title(self.config['title'])

        ax.set_xlabel(self.config['xlabel'])
        ax.set_ylabel(self.config['ylabel'])

        if self.config['showLegend']:
            ax.legend(loc=0)
            #ax.legend(bbox_to_anchor=(0.9,0.9))
        self.canvas.draw()



class LinePlotterDataEditor( QDialog ):

    def __init__( self, parent, data ):
        self.data = data
        super( LinePlotterDataEditor, self ).__init__(parent)
        uic.loadUi( os.path.join(os.path.dirname(__file__), 'LinePlotterDataEditor.ui'), self )
        if len(data) == 0:
            self.newTab()
        else:
            self.applyData()

    @pyqtSlot(int)
    def on_tab_tabCloseRequested(self, index):
        self.tab.removeTab(index)
        if index == 0:
            self.newTab()

    @pyqtSlot()
    def on_btnNewTab_clicked(self):
        self.newTab()

    @pyqtSlot()
    def on_btnSave_clicked(self):
        self.saveData()
        self.close()

    @pyqtSlot()
    def on_btnCancel_clicked(self):
        self.close()

    def newTab(self):
        title = u'线'+unicode(self.tab.count()+1)
        index = self.tab.addTab(LinePlotterDataSpec(), title)
        self.tab.setCurrentIndex(index)

    def saveData(self):
        del self.data[:]
        for i in xrange(self.tab.count()):
            w = self.tab.widget(i)
            self.data.append(w.data())

    def applyData(self):
        for d in self.data:
            title = u'线'+unicode(self.tab.count()+1)
            self.tab.addTab(LinePlotterDataSpec(data=d), title)


class LinePlotterDataSpec( QFrame ):

    _lineStyles = ['-', '--', ':', '-.', 'None']

    def __init__( self, data=None ):
        super( LinePlotterDataSpec, self ).__init__()
        uic.loadUi( os.path.join(os.path.dirname(__file__), 'LinePlotterDataSpec.ui'), self )
        self.lineColor = [0,0,0]
        if data is not None:
            self.applyData(data)

    @pyqtSlot()
    def on_btnLineColor_clicked(self):
        old = QColor()
        old.setRedF(self.lineColor[0])
        old.setGreenF(self.lineColor[1])
        old.setBlueF(self.lineColor[2])
        c = QColorDialog.getColor(old, self)
        if c.isValid():
            self.lineColor = [c.redF(), c.greenF(), c.blueF()]

    def data(self):
        d = {}
        d['ydata'] = np.loadtxt(StringIO( self.txtData.toPlainText() ))
        d['label'] = self.txtLabel.text()
        d['linestyle'] = self._lineStyles[self.cbLineStyle.currentIndex()]
        d['linewidth'] = self.spLineWidth.value()
        d['color'] = self.lineColor
        return d

    def applyData(self, data):
        sdata = StringIO()
        np.savetxt(sdata, data['ydata'], fmt='%.3f')
        self.txtData.setText(sdata.getvalue())
        self.txtLabel.setText(data['label'])
        lsindex = self._lineStyles.index(data['linestyle'])
        self.cbLineStyle.setCurrentIndex(lsindex)
        self.spLineWidth.setValue(data['linewidth'])
        self.lineColor = data['color']


if __name__=="__main__":
    app = QApplication( sys.argv )
    f = LinePlotterWindow()
    f.show()
    sys.exit(app.exec_())