#!/usr/bin/env python

import os
import sys

import expandTemplate

import config

#os.chdir(config.L1ProcROOT) # ?

taskFile = 'L1Proc-' + config.L1Version + '.xml'
template = 'L1Proc.xml.template'

configuration = dict(config.__dict__)

retireScript = os.path.join(config.L1ProcROOT, 'retireRun.py')
retireScriptBody = open(retireScript).read()

configuration['retireScriptBody'] = retireScriptBody

expandTemplate.expand(template, taskFile, configuration)

taskFile = os.path.abspath(taskFile)
print >> sys.stderr, "Now upload:"
print >> sys.stderr, taskFile
