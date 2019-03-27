#!/usr/bin/env python

#add in the different nodes
#add multi body

import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import sys
import numpy as np
import warnings
warnings.filterwarnings("ignore")

useddata = open('useddata.csv','w')
def read_arcstats(i):
    line = i.split(',')
    type = (line[1].split('/')[0],line[3])
    dia = line[6]
    nparts = line[4]
    conti = line[12]
    fin = line[16].replace('\n','')
    time = line[15]
    nclass = line[5]
    lss = float(line[10])
    ias = float(line[11])
    las3d = line[13]
    node = line[8]
    #ignore if a continuation, local searches used, or didn't finish
    if conti == ' false' and fin == 'True' and ias-lss >0 and las3d in (' No','0'):
        useddata.write(i)
        datalist.append((type,nparts,dia,nclass,time))
        print(type,nparts,dia,nclass,time)
testfile = sys.argv[1:]
datalist = []
for i in testfile:
    file = open(i,'r').readlines()
    for j in file[1:]:
        read_arcstats(j)

class2d = []
class3d = []
refine3d = []

for i in datalist:
    if i[0][0] == 'Refine3D' and i[0][1] in ('False','0'):
        refine3d.append(i[1:])
    if i[0][0] == 'Class3D' and i[0][1] in ('False','0'):
        class3d.append(i[1:])
    if i[0][0] == 'Class2D' and i[0][1] in ('False','0'):
        class2d.append(i[1:])

def make_graphs(data,name):
    parts,dia,time,classes = [0],[0],[0],[0]
    for i in data:
        parts.append(float(i[0]))
        dia.append(float(i[1]))
        time.append(float(i[3]))
        classes.append(float(i[2]))
    return(parts,dia,time)


## refine3d
parts,dia,time = make_graphs(refine3d,'r3d')
plt.scatter(parts,time)
polyr3d= (np.polyfit(parts,time,2))
plt.plot(np.polyval(polyr3d,range(int(1.25*max(parts)))))
fe = []
#calculate the fit errors:
for i in zip(time,parts):
    fe.append(i[0]-np.polyval(polyr3d,i[1]))
#print(max(fe))
polyr3d[2] = polyr3d[2]+max(fe)
plt.plot(np.polyval(polyr3d,range(int(1.25*max(parts)))))
plt.savefig('ref3d.png')
plt.close()



##class3d
parts,dia,time = make_graphs(class3d,'c3d')
plt.scatter(parts,time)
polyc3d= (np.polyfit(parts,time,2))
plt.plot(np.polyval(polyc3d,range(int(1.25*max(parts)))))
fe = []
#calculate the fit errors:
for i in zip(time,parts):
    fe.append(i[0]-np.polyval(polyc3d,i[1]))
polyc3d[2] = polyc3d[2]+max(fe)
plt.plot(np.polyval(polyc3d,range(int(1.25*max(parts)))))
plt.savefig('class3d.png')
plt.close()

## class2d
parts,dia,time = make_graphs(class2d,'c2d')
plt.scatter(parts,time)
polyc2d= (np.polyfit(parts,time,2))
plt.plot(np.polyval(polyc2d,range(int(1.25*max(parts)))))
fe = []
#calculate the fit errors:
for i in zip(time,parts):
    fe.append(i[0]-np.polyval(polyc2d,i[1]))
#print(max(fe))
polyc2d[2] = polyc2d[2]+max(fe)
plt.plot(np.polyval(polyc2d,range(int(1.25*max(parts)))))
plt.savefig('class2d.png')
plt.close()

print"""
'Refine3D':[{0}, {1}, {2}],
'Class3D':[{3}, {4}, {5}],
'Class2D':[{6}, {7}, {8}]
""".format(polyr3d[0],polyr3d[1],polyr3d[2],polyc3d[0],polyc3d[1],polyc3d[2],polyc2d[0],polyc2d[1],polyc2d[2])

