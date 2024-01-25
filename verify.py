#!/sdf/group/fermi/a/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

import os
import sys

import config

import pipeline
import runner

cmd = '''
echo 'pipelineSet='
which pipelineSet
echo '------'
'''
status = runner.run(cmd)

pipeline.setVariable('pippa', '2.3')

