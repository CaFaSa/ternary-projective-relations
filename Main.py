import Test
from ternaryRelationsCalculator import *
from Model.Relations import *
from Model.Relations import _SingleProjectiveRelation, _Operations
from gui.polygon_drawer import PolygonDrawer
from gui.polygon_drawer_2 import Drawer

if __name__ == '__main__':
    '''
    Test.run_test_1()
    Test.run_test_2()
    Test.run_test_3()
    Test.run_test_4()
    Test.run_test_5()
    Test.run_test_6()
    Test.run_test_7()
    Test.run_test_8()
    Test.run_test_9()
    Test.run_test_10()
    Test.run_test_11()
    Test.run_test_12()
    Test.run_test_13()
    Test.run_test_14()
    Test.run_test_15()
    '''


    CGU=ComputationalGeometryUtilities() 

    pd = Drawer("Poligon Drawer 2.0")
    pd.run()

    poly1=CGU.createPolygon(pd.polygons[0])
    poly2=CGU.createPolygon(pd.polygons[1])
    poly3=CGU.createPolygon(pd.polygons[2])

    TRC = TernaryRelationCalculator(0, 800,poly1,poly2,poly3)
    TRC.classify()
    TRC.view()

    exit(0)





