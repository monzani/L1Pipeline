
import os
import sys
import xml.dom.minidom as md

import PipelineNetlogger

import config

#log = PipelineNetlogger.PNetlogger.getLogger()
log = PipelineNetlogger.PNetlogger(config.netloggerDest, config.netloggerLevel)

loggableTypes = ['clean', 'error', 'undefined', 'warning']

eventType = '.'.join([os.environ['PIPELINE_TASKPATH'].split('.')[0],
                      os.environ['PIPELINE_PROCESS']])

def parser(inFile):
    doc = md.parse(inFile)
    states = doc.getElementsByTagName('alarmStatistics')
    if len(states) != 1:
        raise ValueError, 'Alarm file %s does not have exactly one statistics tag!' % inFile
    stats = states[0]
    number = {}
    for alarmType in loggableTypes:
        number[alarmType] = int(stats.getAttribute(alarmType))
        continue
    return number


def alarmSeverity(number):
    if number['error'] or number['undefined']:
        severity = log.error
    elif number['warning']:
        severity = log.warn
    else:
        severity = log.info
        pass
    return severity


def doAlarms(inFile, fileType, runId):
    number = parser(inFile)
    severity = alarmSeverity(number)
    head = '%(fileType)s monitoring for run %(runId)s had:  ' % locals()
    message = head + 'data errors:%(error)d, processing errors:%(undefined)d, warnings:%(warning)d, clean:%(clean)d.' % number

    print >> sys.stderr, 'Logging to [%s]' % config.netloggerDest
    print >> sys.stderr, message

    target = 'dk=%s;nR=%s;nD=%s' % (
        fileType,
        os.environ['runNumber'],
        os.environ['DOWNLINK_ID'],
        )

    timeStamp = None
    
    severity(eventType, message, target, timeStamp, config.scid)

    return
