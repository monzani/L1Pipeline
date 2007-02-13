#!/usr/bin/env python

from os import system,environ
 
system("cd ${TestDir}/${CHUNK_ID}; doxygen /afs/slac.stanford.edu/g/glast/ground/PipelineConfig/EM-tasks/builds/TestReport/v3r6p33/src/ReportDoxyfile ; mv *.eps latex/ ; cd latex ; latex refman.tex ; dvips -o refman.ps refman.dvi ; ps2pdf refman.ps refman.pdf; chgrp -R glast-pipeline "+environ['TestDir']+"/"+environ['CHUNK_ID'])

 
