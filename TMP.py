import Test
from ternaryRelationsCalculator import *
from Model.Relations import *
from Model.Relations import _SingleProjectiveRelation, _Operations
from gui.polygon_drawer import PolygonDrawer
from gui.polygon_drawer_2 import Drawer


'''
def composition(T,rowRelation,columnRelations):
    columnList=['bt','rs','bf','ls','af']
    columnRelations=columnRelations.split(":")
    outputSet=set()
    tempSet=set()
    print(len(T.get_subrows(q)))
    for k in range(len(T.get_subrows(q))):
        i=0
        tempSet.clear()
        while i < len(columnRelations):
            secondFactor=ProjectiveRelation(T[row][columnList.index(columnRelations[i+1])])
            if len(tempSet)==0:
                firstFactor=ProjectiveRelation(T[k][columnList.index(columnRelations[i])])
                tempSet=_Operations.product(firstFactor,secondFactor)
            else:
                tempSet=_Operations.product(tempSet,secondFactor)
                i=i+1
        outputSet = outputSet.union(tempSet)

    return outputSet
'''

def composition(r,q):
    T = Table5_composition()
    columnList = ['bt', 'rs', 'bf', 'ls', 'af']
    subRowsList = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    result = None
    daMoltiplicare= []
    risultato=set()

    '''
    Per ogni sottoriga s, salvo in una lista le celle corrispondenti alle relazioni r1,...,rk
    Faccio il prodotto fra di loro, unisco al risultato
    Poi procedo alla sottoriga successiva
    '''
    if r.__eq__("in:ou"):
        pass
    else:
        for i in range(len(T.get_subrows(q))):
            daMoltiplicare= []
            for rel in r.__repr__().split(":"):
                daMoltiplicare.append(T.get_value(str(q),subRowsList[i],str(rel)))
            risultato= risultato.union(moltiplica(daMoltiplicare))


def moltiplica(listaElementiDaMoltiplicare):
    risultato=None
    '''
    Prende gli elementi e li moltiplica fra loro. 
    Al primo giro, essendo
    '''
    for k in range(0,len(listaElementiDaMoltiplicare)):
        for singolaRelazioneDelSet in listaElementiDaMoltiplicare[k]:
            if not risultato:
                #risultato = risultato.union(ProjectiveRelation(singolaRelazioneDelSet).get_relations())
                risultato = ProjectiveRelation(singolaRelazioneDelSet)

            else:
                #risultato = risultato.union(_Operations.product(ProjectiveRelation(risultato),ProjectiveRelation(singolaRelazioneDelSet)).get_relations())
                risultato.product(ProjectiveRelation(singolaRelazioneDelSet))
                print(risultato)
    return risultato


if __name__ == '__main__':
    
    r = ProjectiveRelation("bt:rs")
    q = ProjectiveRelation("bt")
    composition(r,q)
'''
    result = None
    if r.__eq__("in:ou"):
        pass
    else:
        s = T.get_subrows(q)
        indexes = []
        u = []
        primo = True
        current = ProjectiveRelation()
    
        for i in range(len(T.get_subrows(q))):
            for rel in r.__repr__().split(":"):  
                nuova = T.get_value(str(q), subRowsList[i], str(rel))
                print(str(nuova).replace("{", "").replace("}",""))
                r2 = ProjectiveRelation(str(nuova).replace("{", "").replace("}","").replace("'",""))
                if primo:
                    current = r2
                else:
                    current = _Operations.product(current, r2)          
                
            u.append(current)
        print("u: ", u)
'''          
                    
            
