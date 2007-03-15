#!/usr/bin/env python

from os import system,environ

import fileNames
import runner
import stageFiles

import config


files = fileNames.setup(environ['DOWNLINK_ID'], environ['RUNID'], \
                        environ['CHUNK_ID'])

staged = stageFiles.StageSet()

if environ['reportType'] == 'digi':
 system("cd "+files['dirs']['digiMon']+"; doxygen /afs/slac.stanford.edu/g/glast/ground/PipelineConfig/EM-tasks/builds/TestReport/v3r6p33/src/ReportDoxyfile ; mv *.eps latex/ ; cd latex ; latex refman.tex ; dvips -o refman.ps refman.dvi ; ps2pdf refman.ps refman.pdf; chgrp -R glast-pipeline "+files['dirs']['digiMon'])
else:
 system("cd "+files['dirs']['reconMon']+"; doxygen /afs/slac.stanford.edu/g/glast/ground/PipelineConfig/EM-tasks/builds/TestReport/v3r6p33/src/ReportDoxyfile ; mv *.eps latex/ ; cd latex ; latex refman.tex ; dvips -o refman.ps refman.dvi ; ps2pdf refman.ps refman.pdf; chgrp -R glast-pipeline "+files['dirs']['reconMon'])

 
