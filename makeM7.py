#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import sys
import os

import config

import GPLinit

import fileNames
import glastTime
import registerPrep
import runner
import stageFiles

status = 0
finishOption = config.finishOption

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

fileType = 'magic7L1'

staged = stageFiles.StageSet(excludeIn=config.excludeIn)

realOutFile = fileNames.fileName(fileType, dlId, runId, next=True)
stagedOutFile = staged.stageOut(realOutFile)

isocBin = config.isocBin

python = config.python
taskBase = config.hpTaskBase
scid = config.scid

tStart = glastTime.met2Iso8860(float(os.environ['tStart']) - config.m7Pad)
tStop = glastTime.met2Iso8860(float(os.environ['tStop']) + config.m7Pad)

arch = config.l0Archive

cmd = """eval `%(isocBin)s/isoc env --add-env=flightops`
export LD_PRELOAD=$ISOC_INSTALLROOT/lib/libXrdPosixPreload.so
%(python)s %(taskBase)s/scripts/DiagRet.py --scid %(scid)s -b "%(tStart)s" -e "%(tStop)s" --lsm --arch %(arch)s | grep -E 'ATT|ORB' > %(stagedOutFile)s
""" % locals()

status = runner.run(cmd)

if status: finishOption = 'wipe'
status |= staged.finish(finishOption)

if not status: registerPrep.prep(fileType, realOutFile)

sys.exit(status)
