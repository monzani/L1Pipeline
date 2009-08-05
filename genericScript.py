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

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

files = {}

inFileTypes = os.environ['inFileTypes'].split(os.sep)
for fileType in inFileTypes:
    realFile = fileNames.fileName(fileType, *idArgs)
    files[fileType] = staged.stageIn(realFile)
    continue

outFileTypes = os.environ['outFileTypes'].split(os.sep)
for fileType in outFileTypes:
    realFile = fileNames.fileName(fileType, next=True, *idArgs)
    files[fileType] = staged.stageOut(realFile)
    registerPrep.prep(fileType, realFile)
    continue

moduleTable = {
    # 'processName': ('moduleName', 'functionName'),
    # no entry required if all 3 are the same
    'electronMerit': ('filterMerit', 'electronMerit'),
    }

procName = pipeline.getProcess()
modName, funcName = moduleTable.get(procName) or (procName, procName)
module = __import__(modName)
function = getattr(module, funcName)

args = {
    'files': files,
    'idArgs': idArgs,
    'idPath': idPath,
    'level': level,
    }

status |= function(**args)

if status: finishOption = 'wipe'
status |= staged.finish(finishOption)

sys.exit(status)
