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

runId = os.environ['RUNID']

staged = stageFiles.StageSet()
finishOption = config.finishOption

app = config.apps['makeFT2']

#input file
#for fake FT2 M7
realM7File = os.path.join(os.environ['DOWNLINK_RAWDIR'], 'magic7_%s.txt' % dlId)
stagedM7File = staged.stageIn(realM7File)

#output
fakeFt2File = fileNames.fileName('ft2Fake', dlId, runId, next=True)
stagedFt2FitsFile = staged.stageOut(fakeFt2File)
workDir = os.path.dirname(stagedFt2FitsFile)
stagedFt2TxtFile = os.path.join(workDir, 'junkFT2.txt')

setupScript = config.packages['ft2Util']['setup']

tFormat = '%.17g'
tStart = tFormat % (float(os.environ['tStart']) - config.ft2Pad)
tStop = tFormat % (float(os.environ['tStop']) + config.ft2Pad)
# ' -DigiTstart %(tStart)s -DigiTstop %(tStop)s'

cmd = '''
cd %(workDir)s
source %(setupScript)s
%(app)s -M7File %(stagedM7File)s -FT2_txt_File %(stagedFt2TxtFile)s -FT2_fits_File %(stagedFt2FitsFile)s --Gleam
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
