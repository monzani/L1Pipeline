#!/usr/bin/env python

import sys

import expandTemplate

import config

L1Version = config.L1Version
maxCpu = config.maxCpu

taskFile = 'L1Proc.xml'
template = taskFile + '.template'
expandTemplate.expand(template, taskFile, locals())

print >> sys.stderr, "Now upload", taskFile
