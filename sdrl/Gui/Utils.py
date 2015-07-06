#-*- coding: utf-8 -*-
from sdrl.Gui.Agents.CommonAgentDialog import CommonAgentDialog
from sdrl.Gui.Representations.RBF import RBFDialog
from sdrl.Gui.Representations.Tabular import TabularDialog
from sdrl.Gui.Policies.eGreedy import eGreedyDialog

from rlpy.Representations import *
from rlpy.Agents import *
from rlpy.Policies import *
from rlpy.Experiments import *

import matplotlib

'''
所有设置窗口全放在这里
没有参数设置的设为None
'''
DialogMapping = {'QLearning':CommonAgentDialog,
                 'Sarsa':CommonAgentDialog,
                 'Greedy_GQ':CommonAgentDialog,
                 'RBF':RBFDialog,
                 'Tabular':TabularDialog,
                 'eGreedy':eGreedyDialog,
                 'UniformRandom':None,
                 'Gibbs':None,
                 }

class RepresentationFactory(object):
    @staticmethod
    def get(config, name, domain):
        if name in config:
            config = config[name]
        if name == 'Tabular':
            return Tabular(domain, discretization=config['discretization'])
        elif name == 'RBF':
            pass

class PolicyFactory(object):
    @staticmethod
    def get(config, name, representation):
        if name in config:
            config = config[name]
        if name == 'eGreedy':
            return eGreedy(representation, epsilon=config['epsilon'])
        elif name == 'UniformRandom':
            return UniformRandom(representation)
        elif name == 'Gibbs':
            return GibbsPolicy(representation)

class AgentFactory(object):
    @staticmethod
    def _commonAgentGet(config, name, representation, policy, agentClass):
        '''通用Agent的get'''
        return agentClass(representation=representation, policy=policy,
                   discount_factor=config['gamma'],
                   initial_learn_rate=config['alpha'],
                   learn_rate_decay_mode=config['alpha_decay_mode'], boyan_N0=config['boyan_N0'],
                   lambda_=config['lambda'])

    @staticmethod
    def get(config, name, representation, policy):
        if name in config:
            config = config[name]
        if name == 'QLearning':
            return AgentFactory._commonAgentGet(config, name, representation, policy, Q_Learning)
        elif name == 'Sarsa':
            return AgentFactory._commonAgentGet(config, name, representation, policy, SARSA)
        elif name == 'Greedy_GQ':
            return AgentFactory._commonAgentGet(config, name, representation, policy, Greedy_GQ)


class ExperimentFactory(object):
    @staticmethod
    def get(**opt):
        if matplotlib.get_backend().lower() == 'qt4agg':
            from PyQt4 import QtGui
            '''
            当matplotlib的backend使用qt4agg时，interactive mode会卡住
            这里对Experiemnt进行hack，手动处理event loop
            '''
            class QtPlottingExperiment(Experiment):
                '''
                选择hack这个函数是因为它在每个step都会被调用一次
                从而可以在每个画图周期处理event loop
                与函数本身的作用无关
                '''
                def _gather_transition_statistics(self, s, a, sn, r, learning=False):
                    super(QtPlottingExperiment, self)._gather_transition_statistics(s, a, sn, r, learning)
                    QtGui.qApp.processEvents()

            return QtPlottingExperiment(**opt)

        else:
            return Experiment(**opt)
