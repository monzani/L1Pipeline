#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import expandTemplate

import config

#os.chdir(config.L1ProcROOT) # ?

taskFile = os.path.join(config.L1Xml, 'L1Proc-' + config.L1Version + '.xml')
template = os.path.join(config.L1Xml, 'L1Proc.xml.template')

configuration = dict(config.__dict__)

retireScript = os.path.join(config.L1ProcROOT, 'retireRun.py')
configuration['retireScriptBody'] = open(retireScript).read()

placeHolderScript = os.path.join(config.L1ProcROOT, 'placeHolder.py')
configuration['placeHolderBody'] = open(placeHolderScript).read()

registerScript = os.path.join(config.L1ProcROOT, 'registerStuff.py')
configuration['registerBody'] = open(registerScript).read()

expandTemplate.expand(template, taskFile, configuration)

taskFile = os.path.abspath(taskFile)
print >> sys.stderr, "Now upload:"
print >> sys.stderr, taskFile
