#!/bin/bash

mode=$1
runId=$2

pipe=/afs/slac.stanford.edu/u/gl/glast/pipeline-II/prod/pipeline

create="${pipe} -m ${mode} createStream --define runNumber=${runId} flagFT2"
#create="${pipe} -m ${mode} createStream --stream ${runId} --define runNumber=${runId} flagFT2"
rollback="${pipe} -m ${mode} rollbackStream --force flagFT2[${runId}]"

echo ${create}
if ${create} ; then
	echo Stream creation successful.
else
	echo Stream creation failed, attempting rollback...
	echo ${rollback}
	${rollback}
fi
