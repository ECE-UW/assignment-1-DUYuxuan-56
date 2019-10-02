import sys
import re
import copy
import math

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self,x):
        self.x=x

    def setY(self,y):
        self.y=y

def distance(a,b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def is_between(a,c,b):
    return distance(a,c) + distance(c,b) <= distance(a,b)+0.0001

def line_intersection(line1, line2):
    xdiff = (line1[0].getX() - line1[1].getX(), line2[0].getX() - line2[1].getX())
    ydiff = (line1[0].getY() - line1[1].getY(), line2[0].getY()- line2[1].getY())

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None
    temp1=line1[0].getX()*line1[1].getY()-line1[0].getY()*line1[1].getX()
    temp2=line2[0].getX()*line2[1].getY()-line2[0].getY()*line2[1].getX()
    d = (temp1, temp2)
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    pt=Point(0,0)
    pt.x=x
    pt.y=y
    if is_between(line1[0],pt,line1[1])==True and is_between(line2[0],pt,line2[1])==True:
        return pt
    else:
        return None


#print line_intersection((A, B), (C, D))
def intersection(line,line2,graphIntsecSet):
    IntsecSet=[]
    for seg in line:
        for seg2 in line2:
            if line_intersection(seg,seg2)!=None:
                pt=Point(0,0)
                pt=line_intersection(seg,seg2)
                IntsecSet.append(pt)
                if seg[0] not in IntsecSet:
                    IntsecSet.append(seg[0])
                if seg[1] not in IntsecSet:
                    IntsecSet.append(seg[1])
                if seg2[0] not in IntsecSet:
                    IntsecSet.append(seg2[0])
                if seg2[1] not in IntsecSet:
                    IntsecSet.append(seg2[1])
                graphIntsecSet.append([0,pt.getX(),pt.getY()])
    return IntsecSet

def not_in(obj,vertList):
    for pt in vertList:
        if pt.getX()==obj.getX() and pt.getY()==obj.getY():
            return False
    return True

def checkIn(index,list3):
    for ele in list3:
        if index==ele[0]:
            return True

def generate(LineSeg):
    edgeSet=[]
    graphIntsecSet=[]
    vertList=[]
    vertSet=dict()
    temp=[]
    for key,line in LineSeg.items():
        for key2,line2 in LineSeg.items():
            if key!=key2:
                vertList=vertList+intersection(line,line2,graphIntsecSet)
    
    for i in range(len(vertList)):
        if not_in(vertList[i],temp):
            temp.append(vertList[i])

    seen = set()
    newlist = []
    for item in graphIntsecSet:
       t = tuple(item)
       if t not in seen:
           newlist.append(item)
           seen.add(t)

    for i in range(len(temp)):
        vertSet[i+1]=temp[i]
        if newlist!=None:
            flag=False
            for j in range(len(newlist)):
                if temp[i].getX()==newlist[j][1] and temp[i].getY()==newlist[j][2]:
                    flag=True
                    index=j
            if flag:
                newlist[index][0]=i+1
    #vertex part
    print("V={")
    for key,val in vertSet.items():
        print(key),
        print(": ("),
        print("%.2f"%val.getX()),
        print(","),
        print("%.2f"%val.getY()),
        print(")")
    print("}")
    #graph part
    distList=[]
    for key,line in LineSeg.items():
        for seg in line:
            distList=distAcendingList(vertSet,seg)
            for i in range(len(distList)-1):
                if checkIn(distList[i][0],newlist) or checkIn(distList[i+1][0],newlist):
                    edgeSet.append((distList[i][0],distList[i+1][0]))
    print("E={")
    for i,edge in enumerate(edgeSet):
        print("<"),
        print(edge[0]),
        print(","),
        print(edge[1]),
        if i != len(edgeSet) - 1:
            print(">,")
        if i == len(edgeSet) - 1:
            print(">")
    print("}")

def distAcendingList(vertSet,seg):
    distList=[]
    for order,pt in vertSet.items():
        if is_between(seg[0],pt,seg[1]):
            distList.append([order,distance(seg[0],pt)])
        distList.sort(key=lambda l:l[1])
    return distList

def main():
    LineSeg=dict()
    segment=[]
    deepcopy=[]
    temp=[]
    while True:
        line = sys.stdin.readline()
        if line == '':
            break
        #strName=weber str
        if line[0]=='a':
            #input is integer
            if (re.match( r'^a "([^"]+)" ( *\( *[-+]?\d+ *, *[-+]?\d+ *\)){2,} *$', line)):
                strName=re.search('\"([^"]+)', line).group(1)
                strName=strName.lower()
                segment[:] = []
                strPtSet=re.findall('\(([^)]+)', line)
                #['2,-1', '2,2', '5,5', '5,6', '3,8']
                for i in range(len(strPtSet)-1):
                    pt=Point(0,0)
                    pt2=Point(0,0)
                    temp=strPtSet[i].split(',')
                    pt.setX(float(temp[0]))
                    pt.setY(float(temp[1]))
                    temp=strPtSet[i+1].split(',')
                    pt2.setX(float(temp[0]))
                    pt2.setY(float(temp[1]))
                    segment.append([pt,pt2])
                deepcopy=copy.deepcopy(segment)
                LineSeg[strName]=deepcopy
                continue
        if line[0]=='c':
            if (re.match( r'^c "([^"]+)" ( *\( *[-+]?\d+ *, *[-+]?\d+ *\)){2,} *$', line)):

                strName=re.search('\"([^"]+)', line).group(1)
                strName=strName.lower()
                if LineSeg.has_key(strName):
                    segment[:] = []
                    strPtSet=re.findall('\(([^)]+)', line)
                    #['2,-1', '2,2', '5,5', '5,6', '3,8']
                    for i in range(len(strPtSet)-1):
                        pt=Point(0,0)
                        pt2=Point(0,0)
                        temp=strPtSet[i].split(',')
                        pt.setX(float(temp[0]))
                        pt.setY(float(temp[1]))
                        temp=strPtSet[i+1].split(',')
                        pt2.setX(float(temp[0]))
                        pt2.setY(float(temp[1]))
                        segment.append([pt,pt2])
                    deepcopy=copy.deepcopy(segment)
                    LineSeg[strName]=deepcopy
                else:
                    print("Error:c specified for a street that does not exist.")
                continue
        if line[0]=='r':
            if (re.match( r'^r "([^"]+)" *$', line)):
                strName=re.search('\"([^"]+)', line).group(1)
                strName=strName.lower()
                if LineSeg.has_key(strName):
                    LineSeg.pop(strName)
                else:
                    print("Error:r specified for a street that does not exist.")
                continue
        if line[0]=='g':
            if (re.match( r'^g *$', line)):
                if LineSeg:
                    generate(LineSeg)
                    continue
        print("Error:invalid input!please input again!")
    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()
