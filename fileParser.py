'''
    Fabio Romano <fabio.romano1990@outlook.it>
    Relations File parser - Composition Table
'''
import os


def readFile():
    fname= os.path.join(os.path.dirname(__file__),"data","tcf.txt")
    with open(fname) as f:
        content = f.read()
    content= content[1:]
    return content


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
    try:
        rawContent = readFile()
        table = contentParser(rawContent)
    except:
        print("Unable to parse file 'tcf.txt'.\n")
        exit()

    while True:
        try:
            columnKey=input("Insert column key:\n")
            rowKey=input("Insert row key:\n")
            print("\n\nValue is:\n\n" )
            print(table[columnKey][rowKey])
            print("\n")
        except:
            print("Unable to parse input.")
            exit()


if __name__ == "__main__":
    main()


