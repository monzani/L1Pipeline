#!/usr/bin/env python


import math


def crumble(total, maxChunk):
    nChunks = int(math.ceil(float(total) / maxChunk))
    chunkSize = total / nChunks
    chunks = [chunkSize] * nChunks
    extra = total - chunkSize * nChunks
    for iChunk in range(extra):
        chunks[iChunk] += 1
        pass
    return chunks


if __name__ == "__main__":
    import operator, sys
    total, maxChunk = [int(x) for x in sys.argv[1:]]
    chunks = crumble(total, maxChunk)
    print chunks, reduce(operator.add, chunks)
    
