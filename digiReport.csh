#!/bin/csh 
 
setenv latexHeader '/afs/slac.stanford.edu/g/glast/ground/PipelineConfig/EM-tasks/builds/TestReport/v3r6p33/src/latexHeader.tex' 
setenv testReportVersion 'v3r6p33' 
doxygen /afs/slac.stanford.edu/g/glast/ground/PipelineConfig/EM-tasks/builds/TestReport/v3r6p33/src/ReportDoxyfile 
mv *.eps latex/ 
cd latex 
latex refman.tex 
dvips -o refman.ps refman.dvi 
ps2pdf refman.ps refman.pdf 
