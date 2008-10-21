
import os
import sys
import xml.dom.minidom as md

import config

import l1Logger
import pipeline

logger = l1Logger.logger
#eventType = l1Logger.eventType

loggableTypes = ['clean', 'error', 'undefined', 'warning']

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
        severity = l1Logger.error
    elif number['warning']:
        severity = l1Logger.warn
    else:
        severity = l1Logger.info
        pass
    return severity


def doAlarms(inFile, fileType, dlId, runId):
    number = parser(inFile)
    severity = alarmSeverity(number)
    head = '%(fileType)s monitoring for run %(runId)s in delivery %(dlId)s had:  ' % locals()
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

    tags = {}
    for alarmType, value in number.items():
        varName = 'L1_Alarm_' + alarmType
        pipeline.setVariable(varName, value)
        tagName = 'tag_' + varName
        tags[tagName] = value
        continue

    print >> sys.stderr, tags
    
    severity(message, link=link, tgt=target, **tags)

    return
