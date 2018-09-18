import itertools
import time
import os
from datetime import datetime
from itertools import *


def converse(triplet):
    listaTemp=list(triplet)
    temp=listaTemp[1]
    listaTemp[1]=listaTemp[2]
    listaTemp[2]=temp
    return tuple(listaTemp)


def rotation(triplet):
    listaTemp=list(triplet)
    temp1=listaTemp[0]
    temp2=listaTemp[1]
    listaTemp[0]=listaTemp[2]
    listaTemp[1]=temp1
    listaTemp[2]=temp2
    return tuple(listaTemp)


BT = {"bt"}
RS = {"rs"}
BF = {"bf"}
LS = {"ls"}
AF = {"af"}
IN = {"in"}
OU = {"ou"}


def composition(ternaryRelationsTable,rowRelation,columnRelations):
    columnList=['bt','rs','bf','ls','af']
    columnRelations=columnRelations.split(":")
    outputSet=set()
    tempSet=set()

    for subrow in ternaryRelationsTable[rowRelation]:
        i=0
        tempSet.clear()
        while i < len(columnRelations)-1:
            secondFactor=subrow[columnList.index(columnRelations[i+1])]
            if len(tempSet)==0:
                firstFactor=subrow[columnList.index(columnRelations[i])]
                tempSet=relationsProduct(firstFactor,secondFactor)
            else:
                tempSet=relationsProduct(tempSet,secondFactor)
                i=i+1
        outputSet = outputSet.union(tempSet)

    return outputSet


def relationsProduct(set1,set2):
    listaProdotti=list(product(set1,set2))
    combinedProducts=[]
    if "IMP" in set1 or "IMP" in set2:
        outputSet=set()
        outputSet.add("IMP")
        return outputSet

    for element in listaProdotti:
        newRelation=""
        for relation in element:
            if newRelation == "":
                newRelation=relation
            else:
                newRelation=newRelation + ":" + relation
        combinedProducts.append(newRelation)
    
  
    sortedList=[]
    for element in combinedProducts:
        splittedRelation=element.split(":")
        sortedList.append(bubblesort(splittedRelation))

    outputSet=set()
    for element in sortedList:
        newRelation=""
        for relation in list(bubblesort(set(element))):
            if newRelation == "":
                newRelation=relation
            else:
                newRelation=newRelation + ":" + relation
        outputSet.add(newRelation)
    return outputSet


def bubblesort(iterable):
    seq = list(iterable)
    for passesLeft in range(len(seq)-1, 0, -1):
        for index in range(passesLeft):
            if getRelationValue(seq[index]) < getRelationValue(seq[index + 1]):
                seq[index], seq[index + 1] = seq[index + 1], seq[index]
    return seq                


def getRelationValue(relation):
    if 'bt' in relation:
        return 10
    elif 'rs' in relation:
        return 9
    elif 'bf' in relation:
        return 8
    elif 'ls' in relation:
        return 7
    elif 'af' in relation:
        return 6
    elif 'in' in relation:
        return 5
    elif 'ou' in relation:
        return 4


def delta(*relations):
    stringa = ""
    for i in range(1, len(relations) + 1):
        for x in itertools.combinations(relations, i):
            relation = ""
            for index in range(len(x)):
                relation = relation + list(x[index])[0] + ":"
                stringa = stringa + relation[:-1] + ", "
    
    setToReturn=set()
    stringa=stringa.split(", ")
    for i in range(0,len(stringa)):
        stringa[i]=stringa[i].strip()

    setToReturn=set(stringa)
    setToReturn.remove("")
    return setToReturn


def relationParser(deltaString):
    if  "Dd" in deltaString:
        deltaString= "delta(BT,RS,BF,LS,AF)"
        return eval(deltaString)
    elif "Dc" in deltaString:
        deltaString= "delta(IN,OU)"
        return eval(deltaString)
    elif "DELTA" not in deltaString:
        tempSet=set()
        tempSet.add(deltaString)
        return tempSet
    else:
        deltaString= deltaString.upper().replace("DELTA","delta")
        return eval(deltaString)


def caso1(triplet,elementIndex,permutationList):
    return converse(permutationList[elementIndex])


def caso2(triplet,elementIndex,permutationList):
    return rotation(converse(permutationList[elementIndex]))


def caso3(triplet,elementIndex,permutationList):
    return rotation(permutationList[elementIndex])


def caso4(triplet,elementIndex,permutationList):
    return rotation(rotation(permutationList[elementIndex]))


def caso5(triplet,elementIndex,permutationList):
    return converse(rotation(permutationList[elementIndex]))


functionsList=[caso1,caso2,caso3,caso4,caso5]



def main():
    relationsProduct({'rs:ls','bt'},{'bt:rs:ls','rs:bf:ls'})
    '''
    tripletta=('Z','B','C')
    permutationList=list(itertools.permutations(['B', 'Z', 'C']))
    elementIndex=-1
    for elemento in permutationList:
        if tripletta in permutationList:
            elementIndex=permutationList.index(tripletta)
            break

    if elementIndex != -1:
        print(listaFunzioni[elementIndex-1](tripletta))
    '''

if __name__ == "__main__":
    main()
