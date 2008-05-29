
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


eventType = '.'.join([
    os.environ['PIPELINE_TASKPATH'].split('.')[0],
    pipeline.getProcess(),
    ])

dlNumber = os.environ['DOWNLINK_ID']
runNumber = os.environ['runNumber']
tags = {
    "tag_downlinkId": int(dlNumber),
    "tag_runId": int(runNumber),
    }


def error(message, *args, **kwargs):
    kwargs.update(tags)
    print >> sys.stderr, 'Logging:'
    print >> sys.stderr, 'Level: ERROR'
    print >> sys.stderr, 'eventType:', eventType
    print >> sys.stderr, 'message:', message
    print >> sys.stderr, 'args:', args
    print >> sys.stderr, 'kwargs:', kwargs
    logger.error(eventType, message, *args, **kwargs)
    return

def info(message, *args, **kwargs):
    kwargs.update(tags)
    print >> sys.stderr, 'Logging:'
    print >> sys.stderr, 'Level: INFO'
    print >> sys.stderr, 'eventType:', eventType
    print >> sys.stderr, 'message:', message
    print >> sys.stderr, 'args:', args
    print >> sys.stderr, 'kwargs:', kwargs
    logger.info(eventType, message, *args, **kwargs)
    return

def warn(message, *args, **kwargs):
    kwargs.update(tags)
    print >> sys.stderr, 'Logging:'
    print >> sys.stderr, 'Level: WARN'
    print >> sys.stderr, 'eventType:', eventType
    print >> sys.stderr, 'message:', message
    print >> sys.stderr, 'args:', args
    print >> sys.stderr, 'kwargs:', kwargs
    logger.warn(eventType, message, *args, **kwargs)
    return
