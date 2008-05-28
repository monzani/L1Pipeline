
import os
import sys

import config

import GPLinit

import pipeline
import PipelineNetlogger

if config.testMode:
    flavor = PipelineNetlogger.Flavor.DEVEL
else:
    flavor = PipelineNetlogger.Flavor.PROD
    pass
print >> sys.stderr, 'Using logging flavor %s' % flavor

logger = PipelineNetlogger.PNetlogger.getLogger(flavor)


eventType = '.'.join([pipeline.getTask(), pipeline.getProcess()])

