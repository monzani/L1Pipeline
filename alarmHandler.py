import os
import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import GPLinit

import runner


def alarmHandler(files, idArgs, inFileTypes, level, outFileTypes, workDir, **args):
    assert level == 'run'

    dlId, runId, chunkId, crumbId = idArgs

    # this will choke unless there is exacly 1 member in inFileTypes
    fileType, = inFileTypes
    
    alarmFileType, = outFileTypes

    stagedInFile = files[fileType]

    stagedAlarmFile = files[alarmFileType]

    python = config.python

    package = config.packages['Common']
    l1Setup = config.l1Setup

    if fileType in ['fastMonError','verifyLog','verifyFt1Error','verifyFt2Error','verifyMeritError']:
        app = config.apps['errorHandler']
        exceptionArgs = ''
        refArgs = ''
    else:
        app = config.apps['alarmHandler']
        exceptionFile = config.alarmExceptions[fileType]
        exceptionArgs = '-x %s' % exceptionFile
        refArgs = '-R %s' % config.alarmRefDir
        pass

    configFile = config.alarmConfigs[fileType]

    instDir = config.L1Build
    glastExt = config.glastExt
         
    cmd = '''
    export INST_DIR=%(instDir)s 
    export GLAST_EXT=%(glastExt)s 
    source %(l1Setup)s
    cd %(workDir)s
    %(python)s %(app)s -c %(configFile)s %(exceptionArgs)s %(refArgs)s -o %(stagedAlarmFile)s %(stagedInFile)s
    ''' % locals()

    status = runner.run(cmd)

    return status
