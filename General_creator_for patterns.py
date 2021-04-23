import os
import csv
import numpy as np
from random import randint, choice

os.system('cls' if os.name=='nt' else 'clear')

noRows = int(input("Total cells' number: "))
noCol = int(input("Number of patterns: "))
noOnes = int(input("Number of active cells per patterns: "))
noBorrowedOnes = int(input("Number of active cells which will be copied: "))

patArray = np.zeros((noCol+1, noRows), dtype=int)
posArray = []
cache = []

# This is for the 1st column.
posTemp = []
for i in range(noOnes):
    rPos = randint(0, noRows-1)
    while rPos in cache:
        rPos = randint(0,noRows-1)
    patArray[0][rPos] = 1
    posTemp.append(rPos)
    cache.append(rPos)

posArray.append(posTemp)

noUniqOnes = noOnes - noBorrowedOnes
canBeBrdPos = []
canBeBrdPos.append(posArray[0])

# We create the middle columns.
firstToLasPos = []
numOfNonRndAcesForDonut = 0
for j in range(1, noCol+1):
    posTemp = []
    posCache = [x for x in canBeBrdPos[j-1]]
    for noRndBrd in range(noBorrowedOnes):
        if len(posCache) < 1:
            break
        rndBrd = randint(0, len(posCache)-1)
        brdPos = posCache[rndBrd]
        del posCache[rndBrd]
        
        if j == 1:
            numOfNonRndAcesForDonut += 1
            firstToLasPos.append(brdPos)
        
        patArray[j][brdPos] = 1
        posTemp.append(brdPos)

# We create the donut loop.
    if j == noCol:
        if noBorrowedOnes > 0:
            for i in firstToLasPos:
                numOfNonRndAcesForDonut += 1
                patArray[j][i] = 1
            rndChoicePool = [ x for x in cache[0:9] if x not in firstToLasPos]
            cache = []
            for i in range(noOnes - numOfNonRndAcesForDonut):
                brdPos = choice(rndChoicePool)
                while brdPos in cache:
                    brdPos = choice(rndChoicePool)
                cache.append(brdPos)   
                patArray[j][brdPos] = 1
            break
        else:
            patArray[j] = patArray[0]

    canBeBrdPosTemp = []
    for i in range(noUniqOnes):
        rPos = randint(0, noRows-1)
        while rPos in cache:
            rPos = randint(0,noRows-1)
            if len(cache) == noRows:
                break
        if len(cache) == noRows:
            break
        patArray[j][rPos] = 1
        posTemp.append(rPos)
        canBeBrdPosTemp.append(rPos)
        cache.append(rPos)

    posArray.append(posTemp)
    canBeBrdPos.append(canBeBrdPosTemp)

    # if len(cache) == noRows:
    #     break

# Transpose patArray
patArray = np.delete(patArray, 0, 0)
dotProduct = np.dot(patArray.transpose(), patArray)

print(dotProduct.size)

# Delete the 1st column, because acopy for it is at the end. 
for iIndex, i in enumerate(dotProduct):
    for jIndex, j in enumerate(i):
        if j > 1:
            dotProduct[iIndex][jIndex] = 1
    
# Save the results in two files. The first file is for patterns, and the second file is for the weights.
filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "p_10%Overl_300cells_5patt_10cells_p_p.txt"))
with open(filepath, "w") as f:
    csv_file = csv.writer(f, delimiter=' ', lineterminator='\n')
    csv_file.writerows(patArray.transpose())

filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "w_10%Overl_300cells_5patt_10cells_p_p.txt"))
with open(filepath, "w") as f:
    csv_file = csv.writer(f, delimiter=' ', lineterminator='\n')
    csv_file.writerows(dotProduct)

# filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "p_20%Overl_100cells_10patt_5cells_p_p.txt"))
# with open(filepath, "r") as f:
#     p = f.read()
#     csv_file = csv.writer(f, delimiter=' ', lineterminator='\n')
#      csv_file.writerows(patArray.transpose())


# Create weights in fixed patterns. Save the results in one file
# input = np.loadtxt("p_40%Overl_100cells_5patt_5cells_p_p.txt", dtype = 'i', delimiter=' ')

# print(input)
# print(input.size)


# dotProduct = np.dot(input, input.transpose())
# for iIndex, i in enumerate(dotProduct):
#     for jIndex, j in enumerate(i):
#         if j > 1:
#             dotProduct[iIndex][jIndex] = 1
# print(dotProduct)
# print(dotProduct.size)

# filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "w_40%Overl_100cells_5patt_5cells_p_p.txt"))
# with open(filepath, "w") as f:
#     csv_file = csv.writer(f, delimiter=' ', lineterminator='\n')
#     csv_file.writerows(dotProduct)
