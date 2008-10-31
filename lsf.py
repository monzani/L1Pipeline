
import bisect
import os
import random
import re
import string
import sys

import config

goodStates = ['ok', 'closed_Full']
#hostsToQuery = 'genfarm'
#hostsToQuery = 'glastcobs glastyilis preemptfarm'


hLRe = re.compile('^HOSTS:(\s+\w+/)+')
hRe = re.compile('\s+(\w+)/')
def getGroups(queue=config.theQ):
    cmd = 'bqueues -l %s' % queue
    lines = [line for line in os.popen(cmd).readlines() if hLRe.match(line)]
    #assert len(lines) == 1
    groups = hRe.findall(lines[0])
    return groups

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
    #cmd = 'bhosts -w %s' % hostsToQuery
    groups = getGroups()
    cmd = ' '.join(['bhosts -w'] + ['%s'] * len(groups)) % tuple(groups)

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
    # not sure this is actually a good idea
    # it optimizes for the single-downlink case
    # but it would be better to randomize them all
    # for multiple downlinks
    totHosts = 0
    totCores = 0
    totCpu = 0.0
    for ht in sorted(types.keys(), key=lambda x:types[x]):
        hl = hostsByType[ht]
        nht = len(hl)
        slots, factor = types[ht]
        totHosts += nht
        cores = nht * slots
        totCores += cores
        cpu = nht * slots * factor
        totCpu += cpu
        print >> sys.stderr, '%s: %d hosts %d cores %f cpu' % (ht, nht, cores, cpu)
        # randomize order of hosts of the same type
        random.shuffle(hl)
        hosts.extend((host,)+types[ht] for host in hl)
        continue
    # We often get multiple deliveries.  Shuffle the whole thing.
    random.shuffle(hosts)

    print >> sys.stderr, 'TOTAL: %d hosts %d cores %f cpu' % (totHosts, totCores, totCpu)
    # put more-desireable hosts at the front of the list
    hosts.reverse()
    
    return hosts


maxSlots = 30
maxHosts = 10
def doBalance(chunks):
    groups = getGroups()
    allHosts = ' '.join(groups)
    hosts = hostList()
    buckets = [[0, ic, chunk, []] for ic, chunk in enumerate(chunks)]
    full = []
    lists = [buckets, full]
    # ic ensures that buckets is presorted while preserving the original
    # order of chunks within groups that are assigned the same number of slots
    # and lets us recover the original order
    for host, slots, factor in hosts:
        try:
            least = buckets.pop(0)
        except IndexError:
            break
        least[0] += slots
        least[-1].append(host)
        nHosts = len(least[-1])
        condition = (least[0] >= maxSlots) or (nHosts >= maxHosts)
        which = lists[condition]
        bisect.insort(which, least)
        continue
    buckets += full
    outies = [None] * len(chunks)
    for slots, ic, chunk, cHosts in buckets:
        outies[ic] = (chunk, makeMList(cHosts, allHosts))
        continue
    return outies

def dontBalance(chunks):
    groups = getGroups()
    mList = ' '.join(groups)
    outies = [(chunk, mList) for chunk in chunks]
    return outies

balance = doBalance


def makeMList(hosts, backup):
    if hosts:
        nHosts = len(hosts)
        prefs = ['%s+%d' % (host, nHosts-ih)
                 for ih, host in enumerate(hosts)]
        prefs.append('others')
        prefStr = ' '.join(prefs)
    else:
        return backup
    return prefStr

