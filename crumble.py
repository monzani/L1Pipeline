#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5


import math


def crumble_equal(total, maxCrumb):
    total = int(total)
    nCrumbs = int(math.ceil(float(total) / maxCrumb))
    crumbSize = total / nCrumbs
    extra = total - crumbSize * nCrumbs
    crumbs = [crumbSize + 1] * extra + [crumbSize] * (nCrumbs - extra)
    return crumbs


def crumble_exp(total, maxCrumb):
    nCrumbs = 7
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


crumble = crumble_exp

if __name__ == "__main__":
    import operator, sys
    total, maxCrumb = [int(x) for x in sys.argv[1:]]
    crumbs = crumble(total, maxCrumb)
    print crumbs, reduce(operator.add, crumbs)
    
