#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5


import math


def crumble(total, maxChunk):
    total = int(total)
    nChunks = int(math.ceil(float(total) / maxChunk))
    chunkSize = total / nChunks
    extra = total - chunkSize * nChunks
    chunks = [chunkSize + 1] * extra + [chunkSize] * (nChunks - extra)
    return chunks


if __name__ == "__main__":
    import operator, sys
    total, maxChunk = [int(x) for x in sys.argv[1:]]
    chunks = crumble(total, maxChunk)
    print chunks, reduce(operator.add, chunks)
    
