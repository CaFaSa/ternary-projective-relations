import Test
from ternaryRelationsCalculator import *
from Model.Relations import *
from Model.Relations import _SingleProjectiveRelation, _Operations
from gui.polygon_drawer import PolygonDrawer
from gui.polygon_drawer_2 import Drawer

if __name__ == '__main__':
    
    r = ProjectiveRelation("bt")
    q = ProjectiveRelation("bt")
    T = Table5_composition()
    columnList = ['bt', 'rs', 'bf', 'ls', 'af']
    subRowsList = ['a', 'b', 'c', 'd', 'e', 'f', 'g']


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
            
                    
            
