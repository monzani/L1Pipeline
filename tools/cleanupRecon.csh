#!/bin/tcsh

set junkDir=~/scratchJunk
mkdir -p $junkDir
cd $junkDir

# this should be all hosts eligible for glastdataq jobs
set hosts=`bhosts -w glastyilis glastcobs preemptfarm | awk 'NR>1&&/ok|closed_Full/{print $1}' | sort | uniq`

foreach host ($hosts)
	bsub -q express -m $host -o $host $L1ProcROOT/tools/_cleanupOne.csh
end
