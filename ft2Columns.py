

qualityMap = {
    'Bad': 0,
    'Good': 1,
    'Good with bad parts': 1,
    'Under review': 1,
    }

def qualityFlag(qualStr):
    return qualityMap[qualStr]

def configFlag(mootAlias):
    if mootAlias.lower().startswith('noms'):
        flag = 1
    else:
        flag = 0
        pass
    return flag
