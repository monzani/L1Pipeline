#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

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

staged = stageFiles.StageSet()
finishOption = config.finishOption

app = config.apps['makeFT2']

#input file
#for FT2 digi merit M7
realDigiFile = fileNames.fileName('digi', dlId, runId)
stagedDigiFile = staged.stageIn(realDigiFile)
realMeritFile = fileNames.fileName('merit', dlId, runId)
stagedMeritFile = staged.stageIn(realMeritFile)
realM7File = os.path.join(os.environ['DOWNLINK_RAWDIR'], 'magic7_%s.txt' % dlId)
stagedM7File=  staged.stageIn(realM7File)

#output
txtFt2File = fileNames.fileName('ft2Txt', dlId, runId, next=True)
stagedFt2TxtFile = staged.stageOut(txtFt2File)

workDir = os.path.dirname(stagedFt2TxtFile)

stagedFt2FitsFile = os.path.join(workDir, 'junkFT2.fits')

setupScript = config.packages['ft2Util']['setup']

realGapFile = os.path.join(
    os.environ['DOWNLINK_RAWDIR'], 'event_gaps_%s.txt' % dlId)
if os.path.exists(realGapFile):
    stagedGapFile =  staged.stageIn(realGapFile)
    gapOpts = ' -Gaps_File %s ' % stagedGapFile
else:
    gapOpts = ''
    pass

datasource = os.environ['DATASOURCE']
if datasource == 'MC':
    mcOpt = '--MC'
else:
    mcOpt = ''
    pass

cmd = '''
cd %(workDir)s
source %(setupScript)s
%(app)s -DigiFile %(stagedDigiFile)s -MeritFile %(stagedMeritFile)s -M7File %(stagedM7File)s -FT2_txt_File %(stagedFt2TxtFile)s -FT2_fits_File %(stagedFt2FitsFile)s %(gapOpts)s %(mcOpt)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
