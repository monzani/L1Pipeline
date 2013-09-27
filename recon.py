#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Reconstruct a crumb.

Really most everything has already been set up at this point. This is just
here to handle staging and set JOBOPTIONS.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import os
import sys

import config

import GPLinit

import fileNames
import fileOps
import pipeline
import runner
import stageFiles

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
chunkId = os.environ['CHUNK_ID']
crumbId = os.environ['CRUMB_ID']

pipeline.setVariable('L1_PI_ID', crumbId)
version = os.environ['PIPELINE_PROCESSINSTANCE']
pipeline.setVariable('L1_PI_version', version)

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

realDigiFile = fileNames.fileName('digi', dlId, runId, chunkId, crumbId)
os.environ['digiChunkFile'] = staged.stageIn(realDigiFile)
realFT2Fake = fileNames.fileName('ft2Fake', dlId, runId, chunkId)
os.environ['fakeFT2File'] = staged.stageIn(realFT2Fake)

realReconFile = fileNames.fileName('recon', dlId, runId, chunkId, crumbId,
                                   version=version)
stagedReconFile = staged.stageOut(realReconFile)
os.environ['reconCrumbFile'] = stagedReconFile
realMeritFile = fileNames.fileName('merit', dlId, runId, chunkId, crumbId,
                                   version=version)
os.environ['meritCrumbFile'] = staged.stageOut(realMeritFile)
realCalFile = fileNames.fileName('cal', dlId, runId, chunkId, crumbId,
                                 version=version)
os.environ['calCrumbFile'] = staged.stageOut(realCalFile)
realGcrFile = fileNames.fileName('gcr', dlId, runId, chunkId, crumbId,
                                 version=version)
os.environ['gcrCrumbFile'] = staged.stageOut(realGcrFile)

workDir = os.path.dirname(stagedReconFile)

dataSource = os.environ['DATASOURCE']

app = config.apps['recon']
options = config.reconOptions[dataSource]
instDir = config.glastLocation
glastExt = config.glastExt

cmd = '''
cd %(workDir)s
export INST_DIR=%(instDir)s 
export GLAST_EXT=%(glastExt)s 
%(app)s %(options)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

if status: # save any core files
    # fugly hack; there should be a facility for this in stageFiles
    print >> sys.stderr, 'Recon failed, looking for core files...'
    pat = os.path.join(workDir, '*core*')
    coreFiles = glob.glob(pat)
    if coreFiles:
        #runDir = fileNames.fileName(None, dlId, runId)
        runDir = os.path.dirname(realReconFile)
        pass
    for cf in coreFiles:
        # and fileOps.copy should accept a directory as the destination
        dest = os.path.join(runDir, os.path.basename(cf))
        fileOps.copy(cf, dest)
        cmd = 'chmod a+r %s' % dest
        runner.run(cmd)
        cmd = 'chmod g+w %s' % dest
        runner.run(cmd)
        continue
    pass

status |= staged.finish(finishOption)

sys.exit(status)
