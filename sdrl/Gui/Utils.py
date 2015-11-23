#-*- coding: utf-8 -*-
from sdrl.Gui.Agents.CommonAgentDialog import CommonAgentDialog
from sdrl.Gui.Representations.RBF import RBFDialog
from sdrl.Gui.Representations.Tabular import TabularDialog
from sdrl.Gui.Representations.KernelizediFDD import KernelizediFDDDialog
from sdrl.Gui.Representations.iFDD import iFDDDialog
from sdrl.Gui.Representations.TileCoding import TileCodingDialog
from sdrl.Gui.Policies.eGreedy import eGreedyDialog
from sdrl.Gui.Policies.SwimmerPolicy import SwimmerPolicyDialog


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
                 'KernelizediFDD':KernelizediFDDDialog,
                 'IncrementalTabular':TabularDialog,
                 'IndependentDiscretization':TabularDialog,
                 'TileCoding':TileCodingDialog,
                 'iFDD':iFDDDialog,
                 'eGreedy':eGreedyDialog,
                 'SwimmerPolicy':SwimmerPolicyDialog,
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
        elif name == 'IncrementalTabular':
            return IncrementalTabular(domain, discretization=config['discretization'])
        elif name == 'IndependentDiscretization':
            return IndependentDiscretization(domain, discretization=config['discretization'])
        elif name == 'RBF':
            return RBF(domain, num_rbfs=config['num_rbfs'],
                         resolution_max=config['resolution_max'], resolution_min=config['resolution_min'],
                         const_feature=False, normalize=True, seed=1)
        elif name == 'KernelizediFDD':
            return KernelizediFDD(domain,sparsify=config['sparsify'],
                                  kernel=config['kernel'],kernel_args=config['kernel_args'],
                                  active_threshold=config['active_threshold'],
                                  discover_threshold=config['discover_threshold'],
                                  max_active_base_feat=config['max_active_base_feat'],
                                  max_base_feat_sim=config['max_base_feat_sim'])
        elif name == 'iFDD':
            initial_rep = IndependentDiscretization(domain)
            return iFDD(domain, discovery_threshold=config['discover_threshold'],initial_representation=initial_rep,discretization=config['discretization'],iFDDPlus=1 - 1e-7)
        elif name == 'TileCoding':
            return TileCoding(domain, memory = config['memory'], num_tilings=config['num_tilings'])


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
        elif name == 'SwimmerPolicy':
            return SwimmerPolicy.SwimmerPolicy(representation, epsilon=config['epsilon'])       

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
