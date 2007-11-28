
import os
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
    nHosts = {}
    hosts = []
    for line in lines:
        hostName = line[0]
        ht = hostType(hostName)
        if ht not in types:
            types[ht] = hostInfo(hostName)
            pass
        hosts.append(types[ht] + (hostName,))
        nHosts[ht] = nHosts.get(ht, 0) + 1
        continue
    for ht, num in nHosts.items():
        print >> sys.stderr, '%s: %d hosts' % (ht, num)
        continue

    # sort by (slots, cpuf)
    hosts.sort()
    
    return hosts

