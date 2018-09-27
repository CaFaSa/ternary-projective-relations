import Test
from ternaryRelationsCalculator import *
from Model.Relations import *
from Model.Relations import _SingleProjectiveRelation, _Operations
from gui.polygon_drawer import PolygonDrawer
from gui.polygon_drawer_2 import Drawer



def composition(r,q):
    T = Table5_composition()
    columnList = ['bt', 'rs', 'bf', 'ls', 'af']
    subRowsList = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    result = set()
    
    '''
    Per ogni sottoriga s, salvo in una lista le celle corrispondenti alle relazioni r1,...,rk
    Faccio il prodotto fra di loro, unisco al risultato
    Poi procedo alla sottoriga successiva
    PROBLEMA: se q è la riga(ed È la riga)...ed r la colonna(ed r È la colonna)
    richiamando la composition ricorsivamente, dove cavolo li vado a prendere IN e OU sulle COLONNE,
    visto che non ci sono?
    '''
    if "in:ou" in str(r.get_relations()):
        result=result.union(_Operations.product(composition(ProjectiveRelation("in"),ProjectiveRelation(q)),composition(ProjectiveRelation("ou"),ProjectiveRelation(q))).get_relations())
    else:
        for i in range(len(T.get_subrows(q))):
            factors= []
            for rel in r.__repr__().split(":"):
                factors.append(T.get_value(str(q),subRowsList[i],str(rel)))
            product= concatenatedProduct(factors)
            if not product is None:
                result = result.union(product.get_relations())

    return result


def concatenatedProduct(factors):
    result=None
    for factor in factors:
        for singleElement in factor:
            if not result:
                result = ProjectiveRelation(singleElement)
            else:
                result = result.product(ProjectiveRelation(singleElement))

    return result


if __name__ == '__main__':
    
    r = ProjectiveRelation("rs:af")
    q = ProjectiveRelation("bt:rs:ls")
    result=composition(r,q)
    print("Compose result of", r,"°", q, "is:\n",result)
                 
            
