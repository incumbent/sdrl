#-*- coding: utf-8 -*-
import sys
import os
import logging
import traceback

# 将sdrl包路径加入path
fn = os.path.abspath(sys.argv[0])
sdrl_dir = os.path.dirname(fn)
dn = os.path.dirname(sdrl_dir)
if not dn in sys.path:
    sys.path.append(dn)

from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import uic

from sdrl.Gui.Domains.GridWorld import GridWorldFrame
from sdrl.Gui.Domains.MountainCar import MountainCarFrame
from sdrl.Gui.Domains.SystemAdministrator import SystemAdministratorFrame
from sdrl.Gui.Domains.FiftyChain import FiftyChainFrame
from sdrl.Gui.Domains.Pacman import PacmanFrame
from sdrl.Gui.Domains.FiniteTrackCartPole import FiniteTrackCartPoleFrame
from sdrl.Gui.Domains.Swimmer import SwimmerFrame
from sdrl.Gui.Domains.Acrobot import AcrobotFrame
from sdrl.Gui.Domains.Bicycle import BicycleFrame
from sdrl.Gui.Domains.BlocksWorld import BlocksWorldFrame
from sdrl.Gui.Domains.PuddleWorld import PuddleWorldFrame
from sdrl.Gui.Domains.HelicopterHover import HelicopterHoverFrame
from sdrl.Gui.Domains.HIVTreatment import HIVTreatmentFrame
from sdrl.Gui.Domains.PST import PSTFrame
from sdrl.Gui.Domains.ChainMDP import ChainMDPFrame
from sdrl.Gui.Domains.FlipBoard import FlipBoardFrame
from sdrl.Gui.Domains.InfCartPoleBalance import InfCartPoleBalanceFrame
from sdrl.Gui.Domains.IntruderMonitoring import IntruderMonitoringFrame
from sdrl.Gui.Domains.RCCar import RCCarFrame
from sdrl.Gui.Domains.Pinball import PinballFrame

from sdrl.Gui import *
from sdrl.Gui.Utils import ExperimentFactory

# 用于创建子进程，运行实验
import multiprocessing
import threading

import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use('qt4agg')

'''
# 用于Report
import Image
import cStringIO
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.utils import ImageReader
'''


class MainForm( QMainWindow ):
    def __init__( self ):
        super( MainForm, self ).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose) # 保证关闭窗口时不会Crash
        uic.loadUi( os.path.join(sdrl_dir, 'main.ui'), self )
        self.firstOpenExp = True
    
    '''菜单-退出'''
    @pyqtSlot()
    def on_actionExit_triggered(self):
        self.close()

    '''菜单-关于'''
    @pyqtSlot()
    def on_actionAbout_triggered(self):
        d = AboutDialog(self)
        d.setModal(True)
        d.show()

    '''菜单-实验'''
    @pyqtSlot()
    def on_actionGridWorld_triggered(self):
        self.openExperimentTab(GridWorldFrame)
    
    @pyqtSlot()
    def on_actionMountainCar_triggered(self):
        self.openExperimentTab(MountainCarFrame)
    
    @pyqtSlot()
    def on_actionAcrobot_triggered(self):
        self.openExperimentTab(AcrobotFrame)

    @pyqtSlot()
    def on_actionSystemAdministrator_triggered(self):
        self.openExperimentTab(SystemAdministratorFrame)

    @pyqtSlot()
    def on_actionFiftyChain_triggered(self):
        self.openExperimentTab(FiftyChainFrame)

    @pyqtSlot()
    def on_actionSwimmer_triggered(self):
        self.openExperimentTab(SwimmerFrame)

    @pyqtSlot()
    def on_actionPacman_triggered(self):
        self.openExperimentTab(PacmanFrame)

    @pyqtSlot()
    def on_actionFiniteTrackCartPole_triggered(self):
        self.openExperimentTab(FiniteTrackCartPoleFrame)

    @pyqtSlot()
    def on_actionBicycle_triggered(self):
        self.openExperimentTab(BicycleFrame)

    @pyqtSlot()
    def on_actionBlocksWorld_triggered(self):
        self.openExperimentTab(BlocksWorldFrame)

    @pyqtSlot()
    def on_actionPuddleWorld_triggered(self):
        self.openExperimentTab(PuddleWorldFrame)

    @pyqtSlot()
    def on_actionHelicopterHover_triggered(self):
        self.openExperimentTab(HelicopterHoverFrame)

    @pyqtSlot()
    def on_actionHIVTreatment_triggered(self):
        self.openExperimentTab(HIVTreatmentFrame)

    @pyqtSlot()
    def on_actionPST_triggered(self):
        self.openExperimentTab(PSTFrame)
       
    @pyqtSlot()
    def on_actionChainMDP_triggered(self):
        self.openExperimentTab(ChainMDPFrame)
        
    @pyqtSlot()    
    def on_actionFlipBoard_triggered(self):
        self.openExperimentTab(FlipBoardFrame)

    @pyqtSlot()
    def on_actionInfCartPoleBalance_triggered(self):
        self.openExperimentTab(InfCartPoleBalanceFrame)

    @pyqtSlot()
    def on_actionIntruderMonitoring_triggered(self):
        self.openExperimentTab(IntruderMonitoringFrame)

    @pyqtSlot()
    def on_actionRCCar_triggered(self):
        self.openExperimentTab(RCCarFrame)

    @pyqtSlot()
    def on_actionPinball_triggered(self):
        self.openExperimentTab(PinballFrame)
        
    '''菜单-画平面折线图'''
    @pyqtSlot()
    def on_actionLinePlotter_triggered(self):
        from sdrl.Gui.Tools.LinePlotter import LinePlotterWindow
        LinePlotterWindow(self).show()
    
    '''关闭tab标签'''
    @pyqtSlot(int)
    def on_tabTask_tabCloseRequested(self, index):
        self.tabTask.removeTab(index)

    '''当前标签改变'''
    @pyqtSlot(int)
    def on_tabTask_currentChanged(self, index):
        if index >= 0:
            self.loadExperimentConfig(self.tabTask.widget(index).experimentConfig)

    '''运行按钮'''
    @pyqtSlot()
    def on_btnRun_clicked(self):

        opt = {}
        opt['exp_id'] = self.spExpId.value()
        opt['path'] = unicode(self.txtPath.text())

        # 从当前选择的tab的Frame获得domain和agent
        domain, agent = self.tabTask.currentWidget().makeComponents()
        self.currDomain, self.currAgent = domain, agent
        domain.episodeCap = self.spEpisodeCap.value()

        opt['domain'] = domain
        opt['agent'] = agent
        opt["checks_per_policy"] = self.spChecksPerPolicy.value()
        opt["max_steps"] = self.spMaxSteps.value()
        opt["num_policy_checks"] = self.spPolicyChecks.value()

        # 创建子进程运行实验
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=runExperiment, args=(opt, self.chkShowSteps.isChecked(), 
            self.chkShowLearning.isChecked(), self.spShowPerformance.value(), queue))

        dialog = ExpOutputDialog(self, p, queue)
        dialog.setModal(False)
        dialog.show()

        p.start()
        
        self.btnReport.setEnabled(True)


    '''报告按钮'''
    @pyqtSlot()
    def on_btnReport_clicked(self):
        fig = plt.figure(figsize=(4, 3))
        plt.plot([1,2,3,4])
        plt.ylabel('some numbers')

        imgdata = cStringIO.StringIO()
        fig.savefig(imgdata, format='png')
        imgdata.seek(0)  # rewind the data

        Image = ImageReader(imgdata)

        c = canvas.Canvas(os.path.join(unicode(self.txtPath.text()), 'Report.pdf'))
        c.drawImage(Image, cm, cm, inch, inch)
        c.save()

    def openExperimentTab(self, expFrameClass):
        if self.firstOpenExp:
            self.tabTask.removeTab(0)
            self.firstOpenExp = False
        if not self.selectTab(expFrameClass.title):
            self.tabTask.addTab(expFrameClass(), expFrameClass.title)
            self.selectTab(expFrameClass.title)

    def loadExperimentConfig(self, config):
        c = config
        self.chkShowSteps.setChecked(c['showSteps'])
        self.chkShowLearning.setChecked(c['showLearning'])
        self.spShowPerformance.setValue(c['showPerformance'])
        self.spExpId.setValue(c['expId'])
        self.spEpisodeCap.setValue(c['episodeCap'])
        self.spMaxSteps.setValue(c['maxSteps'])
        self.spPolicyChecks.setValue(c['policyChecks'])
        self.spChecksPerPolicy.setValue(c['checksPerPolicy'])
        self.txtPath.setText(c['path'])

    # 根据tabText选择对应tab
    def selectTab(self, tabText):
        for i in xrange(self.tabTask.count()):
            if(self.tabTask.tabText(i) == tabText):
                self.tabTask.setCurrentIndex(i)
                widget = self.tabTask.currentWidget()
                #self.tabTask.setWidth( widget.width() )
                #self.tabTask.setHeight( widget.height() )
                return True
        return False


'''子进程logger的handler'''
class OutputHandler(object):
    def __init__(self, queue):
        super(OutputHandler, self).__init__()
        self.queue = queue
    def handle(self, record):
        self.queue.put(record)


'''
用子进程运行实验的目标函数
由于matplotlib不能在线程中使用，将运算和画图过程放在子进程中
'''
def runExperiment(opt, visualize_steps, visualize_learning, visualize_performance, q):
    # Experiment要在子进程中创建，不能直接传创建好的对象（会影响logger的正常工作）
    exp = ExperimentFactory.get(**opt)

    # 给logger加handler
    # 子进程的log->MemoryHandler->OutputHandler-> queue <-ExpOutputDialog.Receiver->SIGNAL->QTextEdit
    # log通过queue在进程间传递，主线程通过thread接收queue中的新消息
    from logging.handlers import MemoryHandler
    handler = MemoryHandler(capacity=1024, flushLevel=logging.INFO, target=OutputHandler(q))
    exp.logger.addHandler(handler)

    exp.run(visualize_steps=visualize_steps,  # should each learning step be shown?
           visualize_learning=visualize_learning,  # show policy / value function?
           visualize_performance=visualize_performance)  # show performance runs?
    exp.plot()


'''子进程输出窗口'''
class ExpOutputDialog( QDialog ):

    '''接收子进程log的线程'''
    class Receiver(QThread):
        def __init__(self, queue):
            QThread.__init__(self)
            self.queue = queue
        def run(self):
            while True:
                try:
                    record = self.queue.get()
                    self.emit(SIGNAL('newMessage'), record.msg)
                    #self.txtOutput.append(record.msg) # TODO thread unsafe
                except (KeyboardInterrupt, SystemExit):
                    raise
                except EOFError:
                    break
                except:
                    traceback.print_exc()

    def __init__( self, parent, process, queue ):
        super( ExpOutputDialog, self ).__init__(parent)
        uic.loadUi( os.path.join(sdrl_dir, 'Gui', 'ExpOutputDialog.ui'), self )
        # 把窗口放到左上角，以免被实验画图窗口遮住
        geo = self.geometry()
        geo.setX(30)
        geo.setY(50)
        self.setGeometry(geo)
        
        self.process = process
        self.queue = queue
        self.t = self.Receiver(queue)
        self.connect(self.t, SIGNAL('newMessage'), self.appendText)
        self.t.start()
    
    def closeEvent(self, event):
        self.stopExperiment()
        event.accept()

    @pyqtSlot()
    def on_btnStop_clicked(self):
        self.stopExperiment()

    def stopExperiment(self):
        try:
            self.process.terminate()
            self.t = None
        except:
            traceback.print_exc()

    def appendText(self, msg):
        self.txtOutput.append(msg)



if __name__=="__main__": 
    app = QApplication( sys.argv )
    f = MainForm()
    f.show()
    sys.exit(app.exec_())
