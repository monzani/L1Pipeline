#!/bin/bash

deliveries=$*

testBuffer=/afs/slac.stanford.edu/g/glast/ground/PipelineStaging6/halfPipeTest
ctDir=${testBuffer}/chunktokens

for del in ${deliveries} ; do
	echo $del
	cp -R ${del} ${testBuffer}
	rdls=${del}/r0*
	for rdl in ${rdls} ; do
		run=$(basename $rdl)
		rct=${ctDir}/${run}
		mkdir -p ${rct}
		evts=${rdl}/*.evt
		for evt in ${evts} ; do
			chunk=$(basename $evt .evt)
			touch ${rct}/${chunk}
		done
	done	
done