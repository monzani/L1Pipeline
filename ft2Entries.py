#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import meritFiles
import registerPrep
import runner
import stageFiles

import ft2Columns

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

fileType = 'ft2Txt'

app = config.apps['makeFT2']

#input file
#for FT2 digi merit M7
realDigiFile = fileNames.fileName('digi', dlId, runId)
stagedDigiFile = staged.stageIn(realDigiFile)
realMeritFile = fileNames.fileName('merit', dlId, runId)
stagedMeritFile = staged.stageIn(realMeritFile)
#realM7File = os.path.join(os.environ['DOWNLINK_RAWDIR'], 'magic7_%s.txt' % dlId)
#realM7File = os.environ['L1_magic7L1_filename']
realM7File = fileNames.fileName('magic7L1', dlId, runId)
stagedM7File=  staged.stageIn(realM7File)

#output
#txtFt2File = fileNames.fileName(fileType, dlId, runId, next=True)
#stagedFt2TxtFile = staged.stageOut(txtFt2File)
ft2Seconds = fileNames.fileName('ft2Seconds', dlId, runId, next=True)
stagedFt2FitsFile = staged.stageOut(ft2Seconds)

workDir = os.path.dirname(stagedFt2FitsFile)

setupScript = config.packages['ft2Util']['setup']

#realGapFile = os.path.join(
#    os.environ['DOWNLINK_RAWDIR'], 'event_gaps_%s.txt' % dlId)
realGapFile = fileNames.fileName('digiGap', dlId, runId)
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

cmtPath = config.cmtPath
stLibDir = config.stLibDir

# run start and stop from merit file
mStart, mStop = meritFiles.startAndStop(stagedMeritFile)
print >> sys.stderr, 'merit:', mStart, mStop
tStart = mStart - config.ft2Pad
tStop = mStop + config.ft2Pad

liveTimeTolerance = config.ft2liveTimeTolerance
#lTTolOpt = '-LiveTimeTolerance %s' % liveTimeTolerance
lTTolOpt = ''

template = config.ft2Template
templOpt = '-new_tpl %s' % template

qualStr = os.environ['runQuality']
print >> sys.stderr, 'Run quality:', qualStr
dataQuality = ft2Columns.qualityFlag(qualStr)
qualOpt = '-DataQual %d' % dataQuality

mootAlias = os.environ['mootAlias']
print >> sys.stderr, 'MOOT alias:', mootAlias
latConfig = ft2Columns.configFlag(mootAlias)
configOpt = '-LatConfig %d' % latConfig

version = fileNames.version(ft2Seconds)
versOpt = '-Version %d' % version

cmd = '''
cd %(workDir)s
export CMTPATH=%(cmtPath)s
source %(setupScript)s
%(app)s -DigiFile %(stagedDigiFile)s -MeritFile %(stagedMeritFile)s -M7File %(stagedM7File)s -FT2_fits_File %(stagedFt2FitsFile)s %(gapOpts)s %(mcOpt)s -DigiTstart %(tStart).17g -DigiTstop %(tStop).17g %(templOpt)s %(qualOpt)s %(configOpt)s %(lTTolOpt)s %(versOpt)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

if not status:
    #registerPrep.prep(fileType, txtFt2File)
    registerPrep.prep('ft2Seconds', ft2Seconds)
    pass

status |= staged.finish(finishOption)

sys.exit(status)
