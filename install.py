#!/usr/bin/env python

import os
import sys

import expandTemplate

import config

#os.chdir(config.L1ProcROOT) # ?

taskFile = 'L1Proc-' + config.L1Version + '.xml'
template = 'L1Proc.xml.template'
expandTemplate.expand(template, taskFile, config.__dict__)

taskFile = os.path.abspath(taskFile)
print >> sys.stderr, "Now upload:"
print >> sys.stderr, taskFile
