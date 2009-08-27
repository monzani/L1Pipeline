#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Boilerplate

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

import GPLinit

import fileNames
import pipeline
import registerPrep
import stageFiles


moduleTable = {
    # 'processName': ('moduleName', 'functionName', ['cleanupName']),
    # no entry required if process, module, func are the same and no cleanup
    'electronMerit': ('filterMerit', 'electronMerit'),
    'findChunks': ('findChunks', 'findChunks', 'cleanup'),
    'findChunksLci': ('findChunks', 'findChunks', 'cleanup'),
    }

def getFuncs(procName):
    names = moduleTable.get(procName) or (procName, procName)
    modName, mainFunc = names[:2]
    module = __import__(modName)
    function = getattr(module, mainFunc)
    if len(names) > 2:
        clName = names[2]
        cleanupFunc = getattr(module, clName)
    else:
        cleanupFunc = None
        pass
    return function, cleanupFunc


def main():
    status = 0

    head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
    if not dlId: head, dlId = os.path.split(head)
    runId = os.environ.get('RUNID')
    chunkId = os.environ.get('CHUNK_ID')
    crumbId = os.environ.get('CRUMB_ID')
    idArgs = (dlId, runId, chunkId, crumbId)

    idPath = '.'.join((arg for arg in idArgs if arg is not None))

    if runId is None:
        level = 'downlink'
    elif chunkId is None:
        level = 'run'
    elif crumbId is None:
        level = 'chunk'
    else:
        level = 'crumb'
        pass

    procName = pipeline.getProcess()
    function, cleanupFunc = getFuncs(procName)

    staged = stageFiles.StageSet(excludeIn=config.excludeIn)

    files = {}

    args = {
        'files': files,
        'idArgs': idArgs,
        'idPath': idPath,
        'level': level,
        'procName': procName,
        }

    inFileTList = os.environ.get('inFileTypes')
    if inFileTList is not None:
        inFileTypes = inFileTList.split(os.sep)
    else:
        inFileTypes = []
        pass
    for fileType in inFileTypes:
        realFile = fileNames.fileName(fileType, *idArgs)
        try:
            files[fileType] = staged.stageIn(realFile)
        except IOError:
            status |= 1
            finalize(status, args, staged, cleanupFunc)
            pass
        continue

    outFileTList = os.environ.get('outFileTypes')
    if outFileTList is not None:
        outFileTypes = outFileTList.split(os.sep)
    else:
        outFileTypes = []
        pass
    for fileType in outFileTypes:
        realFile = fileNames.fileName(fileType, next=True, *idArgs)
        files[fileType] = staged.stageOut(realFile)
        registerPrep.prep(fileType, realFile)
        continue

    try:
        print >> sys.stderr, 'About to run %s with args %s' % (function, args)
        status |= function(**args)
    except:
        print >> sys.stderr, 'Failed!'
        status |= 1
        pass
    print >> sys.stderr, 'Status = %s' % status
    
    finalize(status, args, staged, cleanupFunc)

    return status


def finalize(status, args, staged, cleanupFunc=None):
    args['status'] = status
    if cleanupFunc is not None: status |= cleanupFunc(**args)
    
    if status:
        finishOption = 'wipe'
    else:
        finishOption = config.finishOption
        pass
    status |= staged.finish(finishOption)
    
    sys.exit(status)
    return


if __name__ == '__main__':
    main()
    pass

