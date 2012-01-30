#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import expandTemplate

import config

import fileNames
import variables

#os.chdir(config.L1ProcROOT) # ?

taskNames = ['forceL1Merge', 'L1Proc', 'noReconMerge', 'setL1Status', 'P130-FT2', 'flagFT2']

scriptNames = {
    'placeHolderBody': 'placeHolder.py',
    'qualityScriptBody': 'getQuality.py',
    'registerBody': 'registerStuff.py',
    'retireScriptBody': 'retireRun.py',
    'runningScriptBody': 'setRunning.py',
    'scanScriptBody': 'scanChunks.py',
    'setupQScriptBody': 'setupQuality.py',
    'statusScriptBody': 'setStatus.py',
    'successScriptBody': 'setSuccessful.py',
    'suggestBody': 'suggestQuality.py',
    'wrapupQScriptBody': 'wrapupQuality.py',
    }

def qualify(name):
    fullPath = os.path.join(config.L1ProcROOT, scriptNames[name])
    return fullPath
def embody_inline(script):
    body = open(script).read()
    return body
def embody_exec(script):
    body = "execfile('%s')" % script
    return body

whichBody = os.environ.get('L1_EMBODY', 'inline')
bodies = {'inline': embody_inline, 'exec': embody_exec}
embody = bodies[whichBody]

scriptBodies = dict((name, embody(qualify(name))) for name in scriptNames)

for taskName in taskNames:
    #taskFile = os.path.join(config.L1Xml, config.fullTaskName + '.xml')
    taskFile = os.path.join(config.L1Xml, taskName + '-' + config.L1Version + '.xml')
    template = os.path.join(config.L1Xml, taskName + '.xml.template')

    configuration = dict(config.__dict__)
    configuration.update(scriptBodies)

    for fileType in fileNames.fileTypes:
        if fileType is None: continue
        nTag = fileType + '_versionName'
        varName = variables.mangleName(fileType, 'ver')
        configuration[nTag] = varName
        group = fileNames.dataCatGroup(fileType)
        path = config.dataCatBase
        vTag = fileType + '_version'
        value = '${datacatalog.getDatasetLatestVersion(RUNID, "%(path)s/"+DATASOURCE, "%(group)s")}' % locals()
        configuration[vTag] = value
        # print vTag, value
        continue

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
ofp.write(bEnv("L1_INSTALL_DIR", config.installRoot))
ofp.write(bEnv("L1_BUILD_DIR", config.L1CmtBase))
ofp.write(bEnv("L1_EMBODY", whichBody))
ofp.write(bEnv("L1_TASK_VERSION", config.L1Version))
ofp.write(bEnv("L1ProcROOT", config.L1ProcROOT))

ofp.write(bEnv("CMTCONFIG", config.cmtConfig))
ofp.write(bEnv("CMTPATH", config.cmtPath))
ofp.write(bEnv("GLAST_EXT", config.glastExt))
ofp.write(bEnv("LATCalibRoot", config.LATCalibRoot))
ofp.write(bEnv("LD_LIBRARY_PATH", config.libraryPath))
ofp.write(bEnv("MALLOC_CHECK_", "0"))
ofp.write(bEnv("PFILES", config.PFILES))
ofp.write(bEnv("PYTHONPATH", config.pythonPath))
ofp.write(bEnv("ROOTSYS", config.rootSys))
ofp.write(bEnv("isocMode", config.isocMode))

#ofp.write('%s\n' % config.isocEnv)

ofp.close()


ofq = open('setup.csh', 'w')

ofq.write('source %s\n' % config.glastSetupCsh)

ofq.write(cEnv("L1_TASK_NAME", config.L1Name))
ofq.write(cEnv("L1_INSTALL_DIR", config.installRoot))
ofq.write(cEnv("L1_BUILD_DIR", config.L1CmtBase))
ofq.write(cEnv("L1_EMBODY", whichBody))
ofq.write(cEnv("L1_TASK_VERSION", config.L1Version))
ofq.write(cEnv("L1ProcROOT", config.L1ProcROOT))

ofq.write(cEnv("CMTCONFIG", config.cmtConfig))
ofq.write(cEnv("CMTPATH", config.cmtPath))
ofq.write(cEnv("GLAST_EXT", config.glastExt))
ofq.write(cEnv("LATCalibRoot", config.LATCalibRoot))
ofq.write(cEnv("LD_LIBRARY_PATH", config.libraryPath))
ofq.write(cEnv("MALLOC_CHECK_", "0"))
ofq.write(cEnv("PFILES", config.PFILES))
ofq.write(cEnv("PYTHONPATH", config.pythonPath))
ofq.write(cEnv("ROOTSYS", config.rootSys))
ofq.write(cEnv("isocMode", config.isocMode))

ofq.close()
