#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.5

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles
import registerPrep

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
chunkId = os.environ.get('CHUNK_ID') # might not be set
crumbId = os.environ.get('CRUMB_ID') # might not be set
idArgs = (dlId, runId, chunkId, crumbId)

if chunkId is None:
    level = 'run'
    next = True
else:
    if crumbId is None:
        level = 'chunk'
    else:
        level = 'crumb'
        pass
    next = False
    pass

inFileType = 'ft1NoDiffRsp'
outFileType = 'ft1BadGti'

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

stSetup = config.stSetup
app = os.path.join('$LIKELIHOODROOT', '$CMTCONFIG', 'gtdiffrsp.exe')

realInFile = fileNames.fileName(inFileType, *idArgs)
stagedInFile = staged.stageIn(realInFile)

realFt2File = fileNames.fileName('ft2Fake', *idArgs)
stagedFt2File = staged.stageIn(realFt2File)

realOutFile = fileNames.fileName(outFileType, next=next, *idArgs)
stagedOutFile = staged.stageOut(realOutFile)

workDir = os.path.dirname(stagedOutFile)

model = config.diffRspModel
irf = config.diffRspIrf

cmtPath = config.stCmtPath

cmd = '''
cd %(workDir)s
export CMTPATH=%(cmtPath)s
source %(stSetup)s
mv %(stagedInFile)s %(stagedOutFile)s
%(app)s scfile=%(stagedFt2File)s evfile=%(stagedOutFile)s srcmdl=%(model)s irfs=%(irf)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if level == 'run' and not status: registerPrep.prep(fileType, realOutFile)

sys.exit(status)
