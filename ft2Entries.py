#!/afs/slac/g/glast/isoc/flightOps/rhel5_gcc41/ISOC_PROD/bin/shisoc python2.6

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

# fileType = 'ft2SecondsNoQual'
fileType = os.environ['outFileType']

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
ft2Seconds = fileNames.fileName(fileType, dlId, runId, next=True)
stagedFt2FitsFile = staged.stageOut(ft2Seconds)

workDir = os.path.dirname(stagedFt2FitsFile)
l1Setup = config.l1Setup
instDir = config.L1Build
glastExt = config.glastExt

#realGapFile = os.path.join(
#    os.environ['DOWNLINK_RAWDIR'], 'event_gaps_%s.txt' % dlId)
realGapFile = fileNames.fileName('digiGap', dlId, runId)
if os.path.exists(realGapFile):
    stagedGapFile =  staged.stageIn(realGapFile)
    gapOpts = ' -gapfile %s ' % stagedGapFile
else:
    gapOpts = ''
    pass

# run start and stop from merit file
mStart, mStop = meritFiles.startAndStop(stagedMeritFile)
print >> sys.stderr, 'merit:', mStart, mStop
tStart = mStart - config.ft2Pad
tStop = mStop + config.ft2Pad

template = config.ft2Template
templOpt = '-templateFT2 %s' % template

qualStr = os.environ['runQuality']
print >> sys.stderr, 'Run quality:', qualStr
dataQuality = ft2Columns.qualityFlag(qualStr)
qualOpt = '-dataquality %d' % dataQuality

mootAlias = os.environ['mootAlias']
print >> sys.stderr, 'MOOT alias:', mootAlias
latConfig = ft2Columns.configFlag(mootAlias)
configOpt = '-latconfig %d' % latConfig

version = fileNames.version(ft2Seconds)
versOpt = '-version %d' % version

procVer = config.ft2SecondsProcVer

igrfExport = config.igrfExport

cmd = '''
cd %(workDir)s
export INST_DIR=%(instDir)s 
export GLAST_EXT=%(glastExt)s
%(igrfExport)s
TIMING_DIR=$GLAST_EXT/extFiles/v0r9/jplephem ; export TIMING_DIR
source %(l1Setup)s
%(app)s -digifile %(stagedDigiFile)s -meritfile %(stagedMeritFile)s -m7file %(stagedM7File)s -ft2file %(stagedFt2FitsFile)s %(gapOpts)s -ft2start %(tStart).17g -ft2stop %(tStop).17g %(templOpt)s %(qualOpt)s %(configOpt)s %(versOpt)s -procVer %(procVer)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status:
    registerPrep.prep(fileType, ft2Seconds)
    pass

sys.exit(status)
