'''
    Fabio Romano <fabio.romano1990@outlook.it>
    Relations File parser
'''
import pickle
import os
from ternaryOperations import composition
from ternaryOperations import relationParser


def readTable(deltasExpanded=True):

    fileName=""
    if(deltasExpanded==True):
        fileName= os.path.join(os.path.dirname(__file__),"data","tableWithDeltasExpanded.pickle")
    else:
        fileName= os.path.join(os.path.dirname(__file__),"data","tableWithCompactNotation.pickle")

    with open(fileName, 'rb') as f:
        return pickle.load(f)


def main():
    table=readTable()
    columnRelations="bt"
    rowRelation="rs"
    print(composition(table,rowRelation,columnRelations))
    input()

    while True:
        try:
            columnList=['bt','rs','bf','ls','af']
            subRowsList=['a','b','c','d','e','f','g']
            rowKey=input("Insert Row key(e.g. bt, rs, etc.):\n")
            subRowKey=input("Insert subrow key(e.g. a,b,c, etc.):\n")
            columnKey=input("Insert column key(e.g. bt,rs,bf,ls,af):\n")
            print("\n\nValue is:\n\n" )
            print(table[str(rowKey)][subRowsList.index(subRowKey)][columnList.index(columnKey)])
            print("\n")
        except:
            print("Unable to parse input.")
            exit()


if __name__ == "__main__":
    main()
