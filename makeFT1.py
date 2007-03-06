#!/usr/bin/env python

from os import system,environ
import sys

import fileNames
import runner
import stageFiles
import pipeline
import config

files = fileNames.setup(environ['DOWNLINK_ID'], environ['RUNID'])

staged = stageFiles.StageSet()

stagedMeritFile = staged.stageIn(files['run']['merit'])
Ft1FilePath = files['run']['ft1']

cmd = 'ST='+config.ST+';export ST;PATH=${ST}/bin:${PATH};GLAST_EXT='+config.glastExt+';export GLAST_EXT; ROOTSYS='+config.rootSys+';export ROOTSYS;PFILES='+config.PFILES+';export PFILES;makeFT1 rootFile='+stagedMeritFile+' fitsFile='+Ft1FilePath

status = runner.run(cmd)

staged.finish()

fileType='ft1'
templist=Ft1FilePath.split('/')
Ft1FileName=templist[len(templist)-1]
logipath='/L1Proc/'+fileType+'/'+Ft1FileName
print "logipath=",logipath,"filepath=",Ft1FilePath
pipeline.setVariable('REGISTER_LOGIPATH', logipath)
pipeline.setVariable('REGISTER_FILEPATH', Ft1FilePath)

sys.exit(status)
