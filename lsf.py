
import os
import random
import string
import sys

goodStates = ['ok', 'closed_Full']
hostsToQuery = 'genfarm'


def hostInfo(hostName):
    cmd = 'bhosts -l %s' % hostName
    
    print >> sys.stderr, 'Examining %s ...' % hostName,
    lines = os.popen(cmd).readlines()
    print >> sys.stderr, 'OK:',

    fields = lines[2].split()
    factor = float(fields[1])
    slots = int(fields[3])
    print >> sys.stderr, '%d cores, CPUF %.2f' % (slots, factor)
    
    return slots, factor


def hostType(hostName):
    ht = hostName.rstrip(string.digits)
    return ht


def hostList():
    # get list of all available hosts
    cmd = 'bhosts -w %s' % hostsToQuery

    print >> sys.stderr, 'Listing available hosts ...',
    lines = os.popen(cmd).readlines()
    print >> sys.stderr, 'OK:',

    lines = [line.split() for line in lines[1:]]
    lines = [line for line in lines if line[1] in goodStates]
    print >> sys.stderr, '%d hosts' % len(lines)
    
    # find host types and info
    types = {}
    hostsByType = {}
    for line in lines:
        hostName = line[0]
        ht = hostType(hostName)
        if ht not in types:
            types[ht] = hostInfo(hostName)
            pass
        hostsByType.setdefault(ht, []).append(hostName)
        continue
    hosts = []
    # sort host types by desireability (cores, factor)
    for ht in sorted(types.keys(), key=lambda x:types[x]):
        hl = hostsByType[ht]
        print >> sys.stderr, ht, '%d hosts' % len(hl)
        # randomize order of hosts of the same type
        random.shuffle(hl)
        hosts.extend((host,)+types[ht] for host in hl)
        continue

    # put more-desireable hosts at the front of the list
    hosts.reverse()
    
    return hosts

