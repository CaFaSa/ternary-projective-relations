import pickle
import os
import atexit

class ValidatorLookupTable:
    table=dict()
    def __init__(self):
        self.table=self.readTable()
        if self.table == None:
            self.table=dict()

    def readTable(self):
        try:
            fileName = os.path.join(os.path.dirname(os.path.dirname(__file__)),"data","validatorLookupTable.pickle")
            with open(fileName, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print("Error loading validatorLookupTable",e )
            print("Starting with empty validatorLookupTable...")
            return None

    def writeTable(self):
        fileName = os.path.join(os.path.dirname(os.path.dirname(__file__)),"data","validatorLookupTable.pickle")
        with open(fileName, 'wb') as f:
            return pickle.dump(self.table,f)

    def insert(self,key,value):
        self.table[key]=value
        

VALIDATORLOOKUPTABLE=ValidatorLookupTable()
#Update Table when program ends normally, without CTRL+C
atexit.register(VALIDATORLOOKUPTABLE.writeTable)