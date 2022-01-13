from matplotlib.colors import rgb2hex
import numpy as np
import sys
import matplotlib.pyplot as plt
import random
import math as m
from numpy.core.numerictypes import ScalarType
from numpy.lib.function_base import iterable
from numpy.typing import _128Bit
np.set_printoptions(threshold=sys.maxsize)
from scipy.ndimage.interpolation import zoom
sze = 10
maxsize = 30
zoom1 = 4
arr = np.random.uniform(size=(sze,sze))
arr = zoom(arr,zoom1)
arr3 = np.copy(arr)
random1 = np.random.default_rng()
plt.imshow(arr)
plt.savefig("graphzoom.jpg")
sys.setrecursionlimit(10**8)
final = np.eye(sze*zoom1)
window = .15
blocknum = 9
block = {}
pop = 8000000

def trace2(a,b, seed):
    global blocknum
    if len(block[blocknum]["areas"]) > maxsize:
        return 0
    final[a][b] = blocknum
    if [a,b] not in block[blocknum]["areas"]:
        block[blocknum]["areas"].append([a,b])
    arr[a][b] = 10000
    try:
            if seed * (1+window) > arr[a+1][b] and seed * (1-window) < arr[a+1][b]:
                trace2(a+1,b, seed)
            elif final[a+1][b] not in block[blocknum]["borders"] and final[a+1][b] > 9:
                block[blocknum]["borders"].append(int(final[a+1][b]))
                block[final[a+1][b]]["borders"].append(int(blocknum))
    except IndexError:
        pass

    if seed * (1+window) > arr[a-1][b] and seed * (1-window) < arr[a-1][b] and a-1 > -1:
            trace2(a-1,b, seed)
    elif final[a-1][b] not in block[blocknum]["borders"] and final[a-1][b] > 9 and a-1 > -1:
            block[blocknum]["borders"].append(int(final[a-1][b]))
            block[final[a-1][b]]["borders"].append(int(blocknum))
    
    try:
            if seed * (1+window) > arr[a][b+1] and seed * (1-window) < arr[a][b+1]:
                trace2(a,b+1, seed)
            elif final[a][b+1] not in block[blocknum]["borders"] and final[a][b+1] > 9:
                block[blocknum]["borders"].append(int(final[a][b+1]))
                block[final[a][b+1]]["borders"].append(int(blocknum))
    except IndexError:
        pass
    

    if seed * (1+window) > arr[a][b-1] and seed * (1-window) < arr[a][b-1] and b-1 > -1:       
            trace2(a,b-1, seed) 
    elif final[a][b-1] not in block[blocknum]["borders"] and final[a][b-1] > 9 and b-1 > -1:
            block[blocknum]["borders"].append(int(final[a][b-1]))
            block[final[a][b-1]]["borders"].append(int(blocknum))

def trace(a,b):
    global blocknum
    blocknum += 1
    final[a][b] = blocknum
    seed = arr[a][b]
    arr[a][b] = 10000
    block[blocknum] = {"borders":[],"demo":{},"areas":[], "district":None}
    if [a,b] not in block[blocknum]["areas"]:
        block[blocknum]["areas"].append([a,b])
    try:
            if seed * (1+window) > arr[a+1][b] and seed * (1-window) < arr[a+1][b]:
                trace2(a+1,b, seed)
            elif blocknum == final[a+1][b]:
                trace2(a+1,b,seed)
            elif final[a+1][b] not in block[blocknum]["borders"] and final[a+1][b] > 9:
                block[blocknum]["borders"].append(int(final[a+1][b]))
                block[final[a+1][b]]["borders"].append(int(blocknum))
    except IndexError:
        pass

    if seed * (1+window) > arr[a-1][b] and seed * (1-window) < arr[a-1][b] and a-1 > -1:
            trace2(a-1,b, seed)
    elif blocknum == final[a-1][b]:
            trace2(a-1,b,seed)
    elif final[a-1][b] not in block[blocknum]["borders"] and final[a-1][b] > 9 and a-1 > -1:
            block[blocknum]["borders"].append(int(final[a-1][b]))
            block[final[a-1][b]]["borders"].append(int(blocknum))
    
    try:
            if seed * (1+window) > arr[a][b+1] and seed * (1-window) < arr[a][b+1]:
                trace2(a,b+1, seed)
            elif blocknum == final[a][b+1]:
                trace2(a,b+1,seed)
            elif final[a][b+1] not in block[blocknum]["borders"] and final[a][b+1] > 9:
                block[blocknum]["borders"].append(int(final[a][b+1]))
                block[final[a][b+1]]["borders"].append(int(blocknum))
    except IndexError:
        pass

    if seed * (1+window) > arr[a][b-1] and seed * (1-window) < arr[a][b-1] and b-1 > -1:
            trace2(a,b-1, seed) 
    elif blocknum == final[a][b-1]:
            trace2(a,b-1,seed)
    elif final[a][b-1] not in block[blocknum]["borders"] and final[a][b-1] > 9 and b-1 > -1:
            block[blocknum]["borders"].append(int(final[a][b-1]))
            block[final[a][b-1]]["borders"].append(int(blocknum))
   
for i in range(len(arr)**2):
    a = random.randint(0,len(arr)-1)
    b = random.randint(0,len(arr)-1)
    if arr[a][b] < 9:
        trace(a,b)

for i in range(len(arr)):
    for i2 in range(len(arr[i])):
        if arr[i][i2] > 9: #continues if location is already assigned
            continue
        else:
            trace(i,i2)
        #print(blocknum)

total = 0
total2 = 0
b = blocknum
r1 = 0
d1 = 0
final3 = np.copy(final)
pop1 = np.copy(final)
party = np.copy(final)
for i in range(blocknum-9):
    total = total + len(block[b]["areas"])
    total2 = total2 + len(block[b]["borders"])
    total3 = 0
    borders = 0
    #density
    for i5 in block[b]["borders"]:
        if i5 != b:
            borders += 1
    block[b]["Density"] = round(float(borders/len(block[b]["areas"])),3)
    #population
    base = ((block[b]["Density"] + 1)**2)*2
    int1 = random1.normal(loc=base,scale=10)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    pop = round(abs(int1))
    block[b]["demo"]["pop"] = pop
    #party
    if block[b]["Density"] > 2:
        base2 = ((block[b]["Density"] + 1)**2)/40
        int1 = abs(random1.uniform(abs(base2-.3),base2+.3))
    else:
        base2 = ((block[b]["Density"])*2)/40
        int1 = abs(random1.normal(loc=base2, scale=.1))
    d = float(int1)
    r = float(1-int1)
    block[b]["demo"]["party"] = {"d":round(d,2),"r":round(r,2)}

    #visualize
    for i4 in block[b]["areas"]:
        final3[i4[0]][i4[1]] = block[b]["Density"]
        pop1[i4[0]][i4[1]] = block[b]["demo"]["pop"]
        if block[b]["demo"]["party"]["d"] > block[b]["demo"]["party"]["r"]:
            party[i4[0]][i4[1]] = True
        else:
            party[i4[0]][i4[1]] = False
    d1 = d1 + (block[b]["demo"]["party"]["d"]*block[b]["demo"]["pop"])
    r1 = r1 + (block[b]["demo"]["party"]["r"]*block[b]["demo"]["pop"])

    #Average of randomly assigned values in arr  
    for i2 in block[b]["areas"]:
        total3 = total3 + float(arr3[i2[0]][i2[1]])
    block[b]["AverageVal"] = round(total3/len(block[b]["areas"]),3) 
    
    
    b = b-1


text = False
if text == True:
    for i in range(len(final)):
        for j in range(len(final[i])):
            text = plt.text(j, i, final[i, j],
                       ha="center", va="center", color="black", size=9)

 
check = False
if check == True:
    for i in range(len(final)):
        for i2 in range(len(final)):
            val = final[i][i2]
            try:
                forw = final[i][i2+1]
            except IndexError:
                forw = val
            try:
                if i2 - 1 > -1:
                    back = final[i][i2-1]
                else:
                    back = val
            except IndexError:
                back = val
            if val != forw:
                if forw not in block[val]["borders"] or val not in block[forw]["borders"]:
                    print("epic fail :(" + str(val) + str(forw))
            if val != back:
                if back not in block[val]["borders"] or val not in block[back]["borders"]:
                    print("epic fail (the sequel)" + str(val)+ str(back))
    for i in range(len(final)):
        for i2 in range(len(final)):
            val = final[i][i2]
            try:
                forw = final[i+1][i2]
            except IndexError:
                forw = val
            try:
                if i - 1 > -1:
                    back = final[i-1][i2]
                else:
                    back = val
            except IndexError:
                back = val
            if val != forw:
                if forw not in block[val]["borders"] or val not in block[forw]["borders"]:
                    print("epic fail :(" + str(val) + str(forw))
            if val != back:
                if back not in block[val]["borders"] or val not in block[back]["borders"]:
                    print("epic fail (the sequel)" + str(val)+ str(back))


plt.imshow(final, cmap="rainbow")
plt.tight_layout() 
plt.savefig("blocks.jpg")
plt.imshow(final3, cmap = "rainbow")
plt.tight_layout()
plt.savefig("popbase.jpg")
plt.imshow(pop1, cmap="rainbow")
plt.savefig("pop.jpg")
plt.imshow(party, cmap="Set1")
plt.savefig("party.jpg")
print("# of areas " + str(len(block)))


f = open("data.txt", "w")
f.write(str(block))
f.close()
print("total: " + str(total))
print("average size: " + str(round(total/(blocknum-9), 3)))
print("average borders: " + str(round(total2/(blocknum-9), 3)))
print("d " + str(round(d1)) + " r " + str(round(r1)))

print("creation done")

totalPop = d1 + r1
targetPop = totalPop/10
districtList = np.copy(final)

def areaAssign(list, districtList, name): #assigns all areas in a block to a district
    for i in list:
        districtList[i[0]][i[1]] = name
def grabArea(index): #index is a list
    iter = blocknum
    for i in range(blocknum-9):
        if index in block[iter]["areas"]:
            return iter #returns blocknum
        iter = iter - 1 
    return "no"
    
class district:
    def __init__(self):
        self.contains = []
        self.pop = 0
        self.red = 0
        self.blue = 0
        self.name = None
districts = [i for i in range(10)]
for i in range(len(districts)):
    districts[i] = district()
    districts[i].name = i

block_call, block_name = {}, {}
for key in block:
    for area in block[key]["areas"]:
        block_call[str(area)] = block[key]
        block_name[str(area)] = key


plt.imshow(districtList, cmap="tab10")
plt.savefig("districts.jpg")                                                                                                                                                                                                                                        




