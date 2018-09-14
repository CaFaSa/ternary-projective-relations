'''
    Fabio Romano <fabio.romano1990@outlook.it>
    Relations File parser
'''

import pickle
from ternaryOperations import delta,relationParser


def rowParsing(subRowKey,rowString,startIndex,endIndex):
    subRowKeysValue=dict()


def readFile():
    fname="tabella.tex"
    with open(fname) as f:
        rawContent = f.read()

    rawContent= rawContent.split("hline")[3:]
    cleanContent=[]

    for row in rawContent:
        rowSplittedByColumn = row.split("&")
        for column in rowSplittedByColumn:
            cleanContent.append(column.replace("\\delta","DELTA").replace("%","").replace("$","").replace("\cup","").replace("\\\\\\","").replace("\\s ",":").replace("\\quad","").replace("\\","").replace("cline{3-8}","").replace("r_2backslash r_1","").replace("D_c","Dc").replace("D_d","Dd").strip())
    
    cleaned_file = open("tabellaPulita.txt","w")
    cleaned_file.write(str(cleanContent))
    rows=[]
    lastNumber=0

    for i in range(0,len(cleanContent)):
        if str(cleanContent[i]).isdigit() and i > 0:
            rows.append(cleanContent[lastNumber:i])
            lastNumber=i


    table=dict()
    for row in rows:
        print(row)
        rowKey=row[1]
        listsToAdd=list()
        if 'a' in row:
            listaTemp=list()
            for i in range(3,8):
                listaTemp.append(relationParser(row[i]))
            listsToAdd.append(listaTemp)
        if 'b' in row:
            listaTemp=list()
            for i in range(10,15):
                listaTemp.append(relationParser(row[i]))
            listsToAdd.append(listaTemp)

        if 'c' in row:
            listaTemp=list()
            for i in range(17,22):
                listaTemp.append(relationParser(row[i]))
            listsToAdd.append(listaTemp)
       
        if 'd' in row:
            listaTemp=list()
            for i in range(24,29):
                listaTemp.append(relationParser(row[i]))
            listsToAdd.append(listaTemp)

        if 'e' in row:
            listaTemp=list()
            for i in range(31,36):
                listaTemp.append(relationParser(row[i]))
            listsToAdd.append(listaTemp)
        if 'f' in row:
            listaTemp=list()
            for i in range(38,43):
                listaTemp.append(relationParser(row[i]))
            listsToAdd.append(listaTemp)
        if 'g' in row:
            listaTemp=list()
            for i in range(45,50):
                listaTemp.append(relationParser(row[i]))
            listsToAdd.append(listaTemp)

        table[rowKey]=listsToAdd

    with open("tableWithDeltasExpanded.pickle", 'wb') as f:
        pickle.dump(table, f)


def contentParser(rawContent):
    columns=str(rawContent).split("\n\n\n\n")   #columns are separated with a four newline sequence
    table=dict()
    columnName=""
    for column in columns:
        rows = column.split("\n")
        columnToBeAdded=dict()
        i = 0 
        for row in rows:
            if " " not in row:  #In file tcf.txt, keys do not contain a space in the row
                currentKey=row
                if i == 0 and currentKey:   #To ensure that invalid keyvalues are not taken from the file
                    columnName = currentKey
                    i = i + 1
            else:
                row.split(";")
                #If rowkey already exist, it means its row is continuing, so current value will be added to current cell value
                if currentKey in columnToBeAdded:   
                    columnToBeAdded[currentKey]= columnToBeAdded[currentKey] + row
                else:
                    columnToBeAdded[currentKey]=row
        table[columnName]=columnToBeAdded   #column is added
    return table


def main():
    readFile()
    with open("tableWithDeltasExpanded.pickle", 'rb') as f:
        table = pickle.load(f)
        #print(table["bf:ls:af"][1][0])


if __name__ == "__main__":
    main()


