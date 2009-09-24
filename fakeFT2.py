#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""Should merge this with ft2Entries.
"""

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles
import pipeline
import registerPrep

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)

runId = os.environ.get('RUNID')
chunkId = os.environ.get('CHUNK_ID')

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

app = config.apps['makeFT2']

#input file
#for fake FT2 M7
realM7File = os.path.join(os.environ['DOWNLINK_RAWDIR'], 'magic7_%s.txt' % dlId)
stagedM7File = staged.stageIn(realM7File)

#output
fakeFt2File = fileNames.fileName('ft2Fake', dlId, runId, chunkId, next=True)
runDir = fileNames.fileName(None, dlId, runId)
ft2FakeBase = os.path.basename(fakeFt2File)
permanentFt2File = os.path.join(runDir, ft2FakeBase)
stagedFt2FitsFile = staged.stageOut(fakeFt2File, permanentFt2File)

workDir = os.path.dirname(stagedFt2FitsFile)

setupScript = config.packages['ft2Util']['setup']

tStart = float(os.environ['tStart']) - config.ft2Pad
tStop = float(os.environ['tStop']) + config.ft2Pad

template = config.ft2Template
templOpt = '-new_tpl %s' % template

cmtPath = config.ft2CmtPath
stLibDir = config.stLibDir

cmd = '''
cd %(workDir)s
export CMTPATH=%(cmtPath)s
source %(setupScript)s
%(app)s -M7File %(stagedM7File)s -FT2_fits_File %(stagedFt2FitsFile)s --Gleam --test-quaternion -DigiTstart %(tStart).17g -DigiTstop %(tStop).17g %(templOpt)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
