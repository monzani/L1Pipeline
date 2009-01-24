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

fileType = os.environ['fileType']
inFileType = fileType + 'BadGti'

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

stSetup = config.stSetup
app = os.path.join('$DATASUBSELECTORROOT', '$CMTCONFIG', 'gtmktime.exe')

realInFile = fileNames.fileName(inFileType, *idArgs)
stagedInFile = staged.stageIn(realInFile)

realFt2File = fileNames.fileName('ft2Seconds', *idArgs)
stagedFt2File = staged.stageIn(realFt2File)

realOutFile = fileNames.fileName(fileType, next=next, *idArgs)
stagedOutFile = staged.stageOut(realOutFile)

workDir = os.path.dirname(stagedOutFile)

version = fileNames.version(realOutFile)

filter = 'LIVETIME>0'

cmd = '''
cd %(workDir)s
echo pfiles=[$PFILES]
source %(stSetup)s
echo pfiles=[$PFILES]
%(app)s overwrite=yes roicut=no scfile=%(stagedFt2File)s filter="%(filter)s" evfile=%(stagedInFile)s outFile=%(stagedOutFile)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if level == 'run' and not status: registerPrep.prep(fileType, realOutFile)

sys.exit(status)
