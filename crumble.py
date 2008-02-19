#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief A hideous mess of historical issues.
Function arguments and constants need revision.

"""


import math


def crumble_equal(total, maxCrumb):
    total = int(total)
    nCrumbs = int(math.ceil(float(total) / maxCrumb))
    crumbSize = total / nCrumbs
    extra = total - crumbSize * nCrumbs
    crumbs = [crumbSize + 1] * extra + [crumbSize] * (nCrumbs - extra)
    return crumbs


def crumble_exp_old(total, maxCrumb):
    minCrumbSize = 2500
    maxCrumbs = 7
    minCrumbs = max(1, int(math.floor(float(total) / minCrumbSize)))
    nCrumbs = min(maxCrumbs, minCrumbs)
    factor = 0.95
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
    return crumbSizes


def crumble_exp_new(total, ignored):
    maxCrumb = 4e3 # largest average crumb size
    mmr = 2.0 # largestCrumb / smallestCrumb
    #
    total = int(total)
    nCrumbs = int(math.ceil(float(total) / maxCrumb))
    factor = math.exp(-math.log(mmr) / nCrumbs)
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
    return crumbSizes


crumble = crumble_exp_new

if __name__ == "__main__":
    import operator, sys
    total, maxCrumb = [int(x) for x in sys.argv[1:]]
    crumbs = crumble(total, maxCrumb)
    print crumbs, reduce(operator.add, crumbs)
    
