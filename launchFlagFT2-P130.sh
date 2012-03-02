#!/bin/bash

mode=$1
runNumber=$2

runId=r0${runNumber}

pipe=/afs/slac.stanford.edu/u/gl/glast/pipeline-II/prod/pipeline

create="${pipe} -m ${mode} createStream --define RUNID=${runId} flagFT2-P130"

echo ${create}
${create} && echo Stream creation successful.
