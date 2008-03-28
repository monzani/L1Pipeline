#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import expandTemplate

import config

#os.chdir(config.L1ProcROOT) # ?

taskNames = ['L1Proc', 'lciChunk', 'lciWhole', 'testVerify']

for taskName in taskNames:
    #taskFile = os.path.join(config.L1Xml, config.fullTaskName + '.xml')
    taskFile = os.path.join(config.L1Xml, taskName + '-' + config.L1Version + '.xml')
    template = os.path.join(config.L1Xml, taskName + '.xml.template')

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

    continue

def bEnv(name, value):
    line = '%s="%s" ; export %s\n' % (name, value, name)
    return line

def cEnv(name, value):
    line = 'setenv %s "%s"\n' % (name, value)
    return line

ofp = open('setup.sh', 'w')

ofp.write('source %s\n' % config.glastSetup)

ofp.write(bEnv("L1_TASK_NAME", config.L1Name))
ofp.write(bEnv("L1_TASK_VERSION", config.L1Version))
ofp.write(bEnv("L1_INSTALL_DIR", config.installRoot))
ofp.write(bEnv("L1_BUILD_DIR", config.L1Cmt))

ofp.write(bEnv("CMTCONFIG", config.cmtConfig))
ofp.write(bEnv("CMTPATH", config.cmtPath))
ofp.write(bEnv("GLAST_EXT", config.glastExt))
ofp.write(bEnv("LATCalibRoot", config.LATCalibRoot))
ofp.write(bEnv("LD_LIBRARY_PATH", config.libraryPath))
ofp.write(bEnv("MALLOC_CHECK_", "0"))
ofp.write(bEnv("PFILES", config.PFILES))
ofp.write(bEnv("PYTHONPATH", config.pythonPath))
ofp.write(bEnv("ROOTSYS", config.rootSys))

#ofp.write('%s\n' % config.isocEnv)
