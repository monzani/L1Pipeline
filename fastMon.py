#!/usr/bin/env python

import os
import sys

import config

import fileNames
import runner
import stageFiles


dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
chunkId = os.environ['CHUNK_ID']
files = fileNames.setup(dlId, runId, chunkId)

staged = stageFiles.StageSet()
inFile = staged.stageIn(files['chunk']['event'])
outFile = staged.stageOut(files['chunk']['fastMon'])

package = config.packages['FastMon']

common = config.packages['Common']
commonPy = os.path.join(common['root'], 'python')

os.environ.update(package['env'])

dmRoot = config.L1Cmt
fastMonDir = files['dirs']['fastMon']
os.environ['FAST_MON_DIR'] = fastMonDir

extra = package['extraSetup']
setup = package['setup']
app = config.apps['fastMon']
nEvents = sys.maxint

newLatexDir = config.installBin

cmd = '''
export DATAMONITORING_ROOT=%(dmRoot)s
#export PATH=%(newLatexDir)s:${PATH}
%(extra)s
source %(setup)s
export PYTHONPATH=${PYTHONPATH}:%(fastMonDir)s:%(commonPy)s
echo ____________________ environment ________________________
printenv
echo ____________________ environment ________________________
%(app)s -v -n %(nEvents)d -o %(outFile)s -prf %(inFile)s
''' % locals()

status = runner.run(cmd)
staged.finish()
sys.exit(status)
