#!/afs/slac/g/glast/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

"""@brief A hideous mess of historical issues.
Function arguments and constants need revision.

"""


import math
import sys

import config


def crumble_equal(total):
    maxCrumb = config.crumbSize
    total = int(total)
    nCrumbs = int(math.ceil(float(total) / maxCrumb))
    crumbSize = total / nCrumbs
    extra = total - crumbSize * nCrumbs
    crumbs = [crumbSize + 1] * extra + [crumbSize] * (nCrumbs - extra)
    return crumbs


def crumble_exp_old(total):
    minCrumbSize = config.crumbSize
    maxCrumbs = config.maxCrumbs
    mmr = config.crumbMmr # largestCrumb / smallestCrumb
    minCrumbs = max(1, int(math.floor(float(total) / minCrumbSize)))
    nCrumbs = min(maxCrumbs, minCrumbs)
    print >> sys.stderr, 'nCrumbs = %d' % nCrumbs
    factor = math.exp(-math.log(mmr) / nCrumbs)
    print >> sys.stderr, 'Crumb growth factor = %g' % factor
    scales = []
    totScale = 0
    for iCrumb in range(nCrumbs):
        scale = factor ** iCrumb
        scales.append(scale)
        totScale += scale
        continue
    scales.reverse()
    topCrumb = total / totScale
    crumbSizes = [int(math.ceil(topCrumb * scale)) for scale in scales]
    print >> sys.stderr, crumbSizes
    return crumbSizes


def crumble_exp_new(total):
    maxCrumb = config.crumbSize # largest average crumb size
    mmr = config.crumbMmr # largestCrumb / smallestCrumb
    #
    total = int(total)
    nCrumbs = int(math.ceil(float(total) / maxCrumb))
    print >> sys.stderr, 'nCrumbs = %d' % nCrumbs
    factor = math.exp(-math.log(mmr) / nCrumbs)
    print >> sys.stderr, 'Crumb growth factor = %g' % factor
    scales = []
    totScale = 0
    for iCrumb in range(nCrumbs):
        scale = factor ** iCrumb
        scales.append(scale)
        totScale += scale
        continue
    scales.reverse()
    topCrumb = total / totScale
    crumbSizes = [int(math.ceil(topCrumb * scale)) for scale in scales]
    print >> sys.stderr, crumbSizes
    return crumbSizes


crumble = crumble_exp_old

if __name__ == "__main__":
    import operator, sys
    total = int(sys.argv[1])
    if len(sys.argv) > 2:
        maxCrumb = int(sys.argv[2])
        config.crumbSize = maxCrumb # dirty
        pass
    crumbs = crumble(total)
    print crumbs, reduce(operator.add, crumbs)
    
