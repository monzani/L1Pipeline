#!/sdf/data/fermi/a/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

import os
import sys

import expandTemplate

import config

import fileNames
import variables

#os.chdir(config.L1ProcROOT) # ?

taskNames = ['forceL1Merge', 'L1Proc', 'noReconMerge', 'setL1Status', 'flagFT2', 'testVerifyS3df']

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

