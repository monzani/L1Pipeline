
import os
import sys
import xml.dom.minidom as md

import config

import pipeline

import PipelineNetlogger

if config.testMode:
    flavor = PipelineNetlogger.Flavor.DEVEL
else:
    flavor = PipelineNetlogger.Flavor.PROD
    pass
print >> sys.stderr, 'Using logging flavor %s' % flavor
log = PipelineNetlogger.PNetlogger.getLogger(flavor)

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
    message = head + 'errors:%(error)d, warnings:%(warning)d, clean:%(clean)d, undefined:%(undefined)d.' % number

    print >> sys.stderr, message

    dlNumber = os.environ['DOWNLINK_ID']
    runNumber = os.environ['runNumber']

    target = 'dk=%s;nR=%s;nD=%s' % (
        fileType,
        runNumber,
        dlNumber,
        )
    link = target

    tags = {
        "tag_downlinkId": int(dlNumber),
        "tag_runId": int(runNumber),
        }

    for alarmType, value in number.items():
        varName = 'L1_Alarm_' + alarmType
        pipeline.setVariable(varName, value)
        tagName = 'tag_' + varName
        tags[tagName] = value
        continue

    print >> sys.stderr, tags
    
    severity(eventType, message,
             link=link, tgt=target,
             **tags)

    return
