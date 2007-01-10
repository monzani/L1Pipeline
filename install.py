#!/usr/bin/env python

import sys

import expandTemplate

import config

L1Version = config.L1Version
maxCpu = config.maxCpu

taskFile = 'L1Proc-' + L1Version + '.xml'
template = 'L1Proc.xml.template'
expandTemplate.expand(template, taskFile, locals())

print >> sys.stderr, "Now upload", taskFile
