

qualityMap = {
    'Bad': 0,
    'Good': 1,
    'Good with bad parts': 3,
    'Under review': 2,
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
