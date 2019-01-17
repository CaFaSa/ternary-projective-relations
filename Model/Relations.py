import copy
import itertools
import pickle
import os
from collections import defaultdict
import sys

# Relation's constants
BT = {"bt"}
RS = {"rs"}
BF = {"bf"}
LS = {"ls"}
AF = {"af"}

IN = {"in"}
OU = {"ou"}


SINGLETILESET = set.union(BT, RS, BF, LS, AF, IN, OU)
SINGLETILESET_NO_OVERLAP = set.union(BT, RS, BF, LS, AF)
SINGLETILESET_OVERLAP = set.union(IN, OU)

# Global variables below can not be evaluated atm because delta function is not loaded yet by Python interpreter.
U = None  # delta(bt,rs,bf,ls,af,in,ou)           def10
DD = None  # delta(bt,rs,bf,ls,af)    def 10
DC = None  # delta(in,ou)             def 10

# Need to define tile order to represent basic relations
order = ["bt", "rs", "bf", "ls", "af", "in", "ou"]
five_tiles = ["bt", "rs", "bf", "ls", "af"]
#order_total = ["bt", "rs", "bf", "ls", "af", "bt:rs", "bt:bf", "bt:ls", "bt:af", "rs:bf" "in", "ou"]

order_total = None




# at the moment  classes are not loaded yet. this function will be called at the end of this file
def _set_global_values():
    d = ProjectiveRelation().add_rel_from_CSR("bt,rs,bf,ls,af,in,ou")
    dd = ProjectiveRelation().add_rel_from_CSR("bt,rs,bf,ls,af")
    dc = ProjectiveRelation().add_rel_from_CSR("in,ou")
    global U, DD, DC, order_total
    U = d.delta()
    DD = dd.delta()
    DC = dc.delta()
    order_total = sorted(DD.delta(), key=lambda rel: ProjectiveRelation.order_position(str(rel)))
    order_total.append(ProjectiveRelation(IN))
    order_total.append(ProjectiveRelation(OU))
    order_total.append(ProjectiveRelation("in:ou"))

    # now setting the rotate table
    _Operations._setRotationTable('bt', ProjectiveRelation(ProjectiveRelation("rs:ls").augment(ProjectiveRelation().add_rel_from_CSR("bt,bf").delta()), ProjectiveRelation("bt").augment(ProjectiveRelation().add_rel_from_CSR("rs,ls").delta()), ProjectiveRelation().add_rel_from_CSR("bt,bf").delta(), ProjectiveRelation("bf:af").augment(ProjectiveRelation().add_rel_from_CSR("bt,ls").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation().add_rel_from_CSR("bt,rs").delta()), ProjectiveRelation("bf:ls").augment(ProjectiveRelation("bt")), ProjectiveRelation("rs:bf").augment(ProjectiveRelation("bt")), ProjectiveRelation("bt:af").augment(ProjectiveRelation("ls")), ProjectiveRelation("bt:af").augment(ProjectiveRelation("rs")), DC))
    _Operations._setRotationTable('rs', ProjectiveRelation().add_rel_from_CSR("rs, ou"))
    _Operations._setRotationTable('bf', ProjectiveRelation(ProjectiveRelation("af").augment(ProjectiveRelation("rs,ls").delta()), ProjectiveRelation("rs:ls"), ProjectiveRelation("ou")))
    _Operations._setRotationTable('ls', ProjectiveRelation("ls,ou"))
    _Operations._setRotationTable('af', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("rs,bf,ls").delta()), ProjectiveRelation("rs:ls").augment(ProjectiveRelation("bf"))))

    _Operations._setRotationTable('bt:rs', ProjectiveRelation(ProjectiveRelation("bt,bf").delta().augment(ProjectiveRelation("rs")), ProjectiveRelation("bt").augment(ProjectiveRelation("rs,bf,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("rs")), DC))
    _Operations._setRotationTable('bt:bf', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("rs,bf,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("rs")), ProjectiveRelation("bt").augment(ProjectiveRelation("bf,ls,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("ls")), DC))
    _Operations._setRotationTable('bt:ls', ProjectiveRelation(ProjectiveRelation("bt,bf").delta().augment(ProjectiveRelation("ls")), ProjectiveRelation("bt").augment(ProjectiveRelation("bf,ls,af").delta()), ProjectiveRelation("bf,af").augment(ProjectiveRelation("ls")), DC))
    _Operations._setRotationTable('bt:af', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("rs,bf,ls").delta()), ProjectiveRelation("rs,ls").augment(ProjectiveRelation("bf")), ProjectiveRelation("bf").augment(ProjectiveRelation("bt")), ProjectiveRelation("bf:af").augment(ProjectiveRelation("bt,ls").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("bt,rs").delta()), ProjectiveRelation("bf:ls").augment(ProjectiveRelation("bt")), ProjectiveRelation("rs:bf").augment(ProjectiveRelation("bt")), ProjectiveRelation("bt:af").augment(ProjectiveRelation("ls")), ProjectiveRelation("bt:af").augment(ProjectiveRelation("rs")), DC))
    _Operations._setRotationTable('rs:bf', ProjectiveRelation(ProjectiveRelation("af").augment(ProjectiveRelation("rs")), ProjectiveRelation("ou")))
    _Operations._setRotationTable('rs:ls', ProjectiveRelation(ProjectiveRelation("af"), ProjectiveRelation("bt,bf").delta(), DC))
    _Operations._setRotationTable('rs:af', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("rs,bf").delta()), ProjectiveRelation("rs:bf"), ProjectiveRelation("in,in:ou")))
    _Operations._setRotationTable('bf:ls', ProjectiveRelation(ProjectiveRelation("af").augment(ProjectiveRelation("ls")), ProjectiveRelation("ou")))
    _Operations._setRotationTable('bf:af', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("rs,bf,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("rs")), ProjectiveRelation("bt").augment(ProjectiveRelation("bf,ls,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("ls")), DC))
    _Operations._setRotationTable('ls:af', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("bf,ls").delta()), ProjectiveRelation("bf:ls"), ProjectiveRelation("in,in:ou")))

    _Operations._setRotationTable('bt:rs:bf', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("rs,bf,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("rs")), DC))
    _Operations._setRotationTable('bt:rs:ls', ProjectiveRelation(ProjectiveRelation("bt,bf").delta(), DC))
    _Operations._setRotationTable('bt:rs:af', ProjectiveRelation(ProjectiveRelation("bt,bf").delta(), ProjectiveRelation("rs:bf"), ProjectiveRelation("bt").augment(ProjectiveRelation("rs,bf,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("rs")), DC))
    _Operations._setRotationTable('bt:bf:ls', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("bf,ls,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("ls")), DC))
    _Operations._setRotationTable('bt:bf:af', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("rs,bf,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("rs")), ProjectiveRelation("bt").augment(ProjectiveRelation("bf,ls,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("ls")), DC))
    _Operations._setRotationTable('bt:ls:af', ProjectiveRelation(ProjectiveRelation("bt,bf").delta(), ProjectiveRelation("bf:ls"), ProjectiveRelation("bt").augment(ProjectiveRelation("bf,ls,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("ls")), DC))
    _Operations._setRotationTable('rs:bf:ls', ProjectiveRelation(ProjectiveRelation("af"), DC))
    _Operations._setRotationTable('rs:bf:af', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("rs,bf,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("rs")), DC))
    _Operations._setRotationTable('rs:ls:af', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("bf")), ProjectiveRelation("in, in:ou")))
    _Operations._setRotationTable('bf:ls:af', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("bf,ls,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("ls")), DC))

    _Operations._setRotationTable('bt:rs:bf:ls', DC)
    _Operations._setRotationTable('bt:rs:bf:af', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("rs,bf,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("rs")), DC))
    _Operations._setRotationTable('bt:rs:ls:af', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("bf")), ProjectiveRelation("in,in:ou")))
    _Operations._setRotationTable('bt:bf:ls:af', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("bf,ls,af").delta()), ProjectiveRelation("bf:af").augment(ProjectiveRelation("ls")), DC))
    _Operations._setRotationTable('rs:bf:ls:af', ProjectiveRelation("in,in:ou"))

    _Operations._setRotationTable('bt:rs:bf:ls:af', ProjectiveRelation("in,in:ou"))

    _Operations._setRotationTable('in', ProjectiveRelation(ProjectiveRelation("bt").augment(DD), ProjectiveRelation("rs:ls").augment(DD), ProjectiveRelation("bf:af").augment(DD), DC))
    _Operations._setRotationTable('ou', ProjectiveRelation(ProjectiveRelation("bt").augment(ProjectiveRelation("rs,ls,af").delta()), ProjectiveRelation("rs").augment(ProjectiveRelation("bt,ls,af").delta()), ProjectiveRelation("ls").augment(ProjectiveRelation("bt,rs,af").delta()), ProjectiveRelation("af").augment(ProjectiveRelation("bt,rs,ls").delta()), DC))
    _Operations._setRotationTable('in:ou', ProjectiveRelation(ProjectiveRelation("bt").augment(DD), ProjectiveRelation("rs:ls").augment(DD), ProjectiveRelation("bf:af").augment(DD), DC))


class _SingleProjectiveRelation:
    __relations = set()
    __iterated = []

    def __init__(self, *single_tile_relations):
        for relation in single_tile_relations:
            self.add_rel(relation)

    def __repr__(self):
        sorted_relations = sorted(self.__relations, key=lambda x: order.index(x))
        relation_string = ""
        for r in sorted_relations:
            relation_string = relation_string + r + ":"
        relation_string = relation_string[:-1]

        return relation_string

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __iter__(self):
        return self

    def __next__(self):
        for x in self.__relations:
            if x not in self.__iterated:
                self.__iterated.append(x)
                return x

        self.__iterated = []
        raise StopIteration

    def delta(self):
        return _Operations.delta(self.get_relations())

    def converse(self):
        self = _Operations.converse(self)
        return self

    def rotate(self):
        return _Operations.rotate(self)

    def add_rel(self, *relations):
        self.__relations = set.union(self.__relations, *relations)
        return self

    def add_rel_from_str(self, rel):
        if rel in SINGLETILESET:
            self.add_rel(eval(rel.upper()))
        else:

            raise ValueError(self.__class__,
                             "is trying to use _add_rel_from_str('" + rel + "') but '" + rel + "' is not in SINGLETILESET")


    def get_relations(self):
        return self.__relations

    def remove_relations(self, *relations):
        for r in relations:
            self.__relations.remove(r)


class ProjectiveRelation:
    __relations = set()
    __iterated = []

    def __init__(self, *basic_relations):
        self.add_rel(*basic_relations)
        

    def __repr__(self):
        rel = sorted(self.__relations, key=lambda rel: ProjectiveRelation.order_position(str(rel)))
        relations = ""
        for i in rel:
            relations = relations + str(i) + ", "

        return relations[:-2]

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __iter__(self):
        return self

    def __next__(self):
        for x in self.__relations:
            if x not in self.__iterated:
                self.__iterated.append(x)
                return x

        self.__iterated = []
        raise StopIteration

    @staticmethod
    def order_position(rel: str):
        rel = rel.replace(":", "")
        position = 0
        i=1
        while len(rel) > 0:
            i = i * 10
            position = position + (order.index(str(rel[-2:])) + 1) * i
            rel = rel[:-2]
        #position = position + order.index(str(rel)) +1

        return position + 1

    # INTERSEPTION (ls:bf, ls) e (ls:bf, rs) = ls:bf
    def intersection(self, other_projective_relation):
        if type(other_projective_relation != type(self)):
            other_projective_relation = ProjectiveRelation(other_projective_relation)
        rel = ProjectiveRelation(self.__relations.intersection(other_projective_relation.__relations))
        return rel

    def union(self, other_projective_relation):
        if type(other_projective_relation != type(self)):
            other_projective_relation = ProjectiveRelation(other_projective_relation)
        rel = ProjectiveRelation(self.__relations.union(other_projective_relation.__relations))
        return rel

    def augment(self, other):
        return _Operations.augment(self, other)

    def product(self, other):
        return _Operations.product(self, other)

    def delta(self):
        relations = _SingleProjectiveRelation()
        ret_rel = ProjectiveRelation()

        for r in self.get_relations():
            relations.add_rel(r.get_relations())

        for r in relations.delta().get_relations():
            ret_rel.add_rel(r)
        return ret_rel

    def converse(self):
        conv_object = ProjectiveRelation()
        for r in self.__relations:
            conv_object.add_rel(r.converse())
        return conv_object

    def composition(self, other_rel):
        comp = set()
        relationsList=list(self.__relations)
        otherRelationsList=list(other_rel.__relations)
        for rel1 in relationsList:
            for rel2 in otherRelationsList:
                op_res = _Operations.composition(rel1,rel2)
                comp = comp.union(op_res)
        return ProjectiveRelation(str(comp).replace("{","").replace("}","").replace(" ", "").replace("'", ""))

    def add_rel(self, *basic_relations):
        for r in basic_relations:
            if r=="" or r=="IMP" or r=="imp": #ignores imp relations
                continue
            if str(r).__contains__("{"):
                r=str(r)
            if isinstance(r, _SingleProjectiveRelation):  # check if it is yet a _SingleProjectiveRelation
                self.__relations = set.union(self.__relations, basic_relations)
            elif isinstance(r, str):
                r=r.replace("{","").replace("}","").replace(" ", "").replace("'", "")
                if "," in r:
                    self.add_rel_from_CSR(r)
                else:
                    if str(r) != "set()":  #temp fix for passing empty set as a string (don't know who is doing such)
                        self._add_rel_from_str(r)
            elif isinstance(r, ProjectiveRelation):
                self.__relations = self.__relations.union(r.get_relations())
            else:  # maybe it is a set
                for rel_name in r:
                    tmp = _SingleProjectiveRelation()
                    tmp.add_rel_from_str(str(rel_name))
                    self.add_rel(tmp)

        self.validate_relations()
        return self

    def add_rel_from_CSR(self, CSV: str):
        rel_list = CSV.lstrip().split(",")

        for r in rel_list:
            self.add_rel(r.lstrip())
        return self

    def _add_rel_from_str(self, rel):
        rel = str(rel)
        rel = rel.lower()
        adding_rel = _SingleProjectiveRelation()

        if rel.__len__() > 2:
            relations = rel.split(":")
            for r in relations:
                if r == "" or r == "IMP" or r == "imp":  # ignores imp relations
                    continue
                else:
                    if r.__len__() == 2:
                        adding_rel.add_rel_from_str(r)
                    else:
                        raise ValueError(self.__class__,
                                         "is trying to use _add_rel_from_str('" + rel + "'). The splitted '" + r + " has not length 2")
        else:
            adding_rel.add_rel_from_str(rel)

        self.add_rel(adding_rel)

    def get_relations(self):
        return self.__relations

    def rotate(self):
        ret_rel = ProjectiveRelation()
        for rel in self.__relations:
            ret_rel.add_rel(rel.rotate())

        return ret_rel

    def validate_relations(self):
        to_be_deleted = set()
        for r in self.__relations: #type: _SingleProjectiveRelation
            relation_set = r.get_relations()
            if relation_set.intersection(SINGLETILESET_NO_OVERLAP) and relation_set.intersection(SINGLETILESET_OVERLAP):
                to_be_deleted.add(r)
        if to_be_deleted:
            self.__relations.remove(to_be_deleted.pop())


class _Operations:
    __converse_table = defaultdict(dict)
    __converse_table['bt'] = set.union(BT)
    __converse_table['rs'] = set.union(LS)
    __converse_table['ls'] = set.union(RS)
    __converse_table['bf'] = set.union(AF)
    __converse_table['af'] = set.union(BF)
    __converse_table['in'] = set.union(IN)
    __converse_table['ou'] = set.union(OU)


    __rotation_table = defaultdict(dict)
    __rotation_table['bt'] = None
    __rotation_table['rs'] = None
    __rotation_table['bf'] = None
    __rotation_table['ls'] = None
    __rotation_table['af'] = None
    __rotation_table['in'] = set.union(IN)
    __rotation_table['ou'] = set.union(OU)


    @staticmethod
    def converse(relation: _SingleProjectiveRelation):
        relations = relation.get_relations()
        ret_relation = _SingleProjectiveRelation()

        for i in relations:
            ret_relation.add_rel(_Operations.__converse_table[i])

        return ret_relation

    @staticmethod
    def rotate(relation: _SingleProjectiveRelation):
        ret_relation = ProjectiveRelation()
        ret_relation.add_rel(_Operations.__rotation_table[str(relation)])

        return ret_relation


    @staticmethod
    def delta(relation):
        result = ProjectiveRelation()

        for n in range(len(relation) + 1):
            iterator = itertools.combinations(relation, n + 1)
            partial_rel = _SingleProjectiveRelation()
            if n + 1 == 1:
                for r in iterator:
                    result.add_rel(set(r))
            else:
                for r in iterator:
                    partial_rel = _SingleProjectiveRelation()
                    partial_rel.add_rel(set(r))
                    result.add_rel(partial_rel)
            if len(partial_rel.get_relations()) > 0:
                result.add_rel(partial_rel)

        return result

    @staticmethod
    def product(relation_1: ProjectiveRelation, relation_2: ProjectiveRelation):
        ret_rel = ProjectiveRelation()
        for rel_1 in relation_1.get_relations():
            working_rel = _SingleProjectiveRelation(rel_1.get_relations())
            for rel_2 in relation_2.get_relations():
                working_rel.add_rel(rel_2.get_relations())
                ret_rel.add_rel(working_rel)
                working_rel = _SingleProjectiveRelation(rel_1.get_relations())

        return ret_rel

    @staticmethod
    def augment(first: ProjectiveRelation, other: ProjectiveRelation):
        ret_rel = ProjectiveRelation()
        #sorted(self.__relations, key=lambda rel: ProjectiveRelation.order_position(str(rel)))
        for single_rel_1 in sorted(first.get_relations(), key=lambda rel: ProjectiveRelation.order_position(str(rel))):
            ret_rel.add_rel(single_rel_1)
            for single_rel_2 in sorted(other.get_relations(), key=lambda rel: ProjectiveRelation.order_position(str(rel))):
                rel = _SingleProjectiveRelation(single_rel_1.get_relations())
                rel.add_rel(single_rel_2.get_relations())
                ret_rel.add_rel(rel)

        return ret_rel

    @staticmethod
    def _setRotationTable(row, projectiveRelation: ProjectiveRelation):
        _Operations.__rotation_table[row] = projectiveRelation

    @staticmethod
    def composition(r:ProjectiveRelation, q:ProjectiveRelation):
        T = TABLE5
        inOutColumns_Table4 = TABLE4
        subRowsList = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        result = set()

        if "in:ou" in str(r.get_relations()):
            result = result.union(_Operations.product(inOutColumns_Table4.get_value(q.get_relations(),"in"),inOutColumns_Table4.get_value(q.get_relations(),"ou")).get_relations())
        else:
            for i in range(len(T.get_subrows(q))):
                factors = []
                for rel in r.__repr__().split(":"):
                    factors.append((T.get_value(str(q), subRowsList[i], str(rel))))
                product = concatenatedProduct(factors)
                if not product is None:
                    result = result.union(product.get_relations())

        return result


#TODO: move from global scope
def concatenatedProduct(factors):
    result=None
    factors= list(factors)
    if len(factors)==1:
        result=ProjectiveRelation(factors[0])
    else:
        for i in range(0,len(factors)):
            if not result:
                result = ProjectiveRelation(factors[i])
            else:
                result = result.product(ProjectiveRelation(factors[i]))
    return result


class Table4_in_ou_columns:
    __table = None
    __inColumn=[]
    __ouColumn=[]
    __rowList=["bt","rs","bf","ls","af","bt:rs","bt:bf","bt:ls","bt:af","rs:bf","rs:ls","rs:af","bf:ls","bf:af","ls:af","bt:rs:bf","bt:rs:ls","bt:rs:af","bt:bf:ls","bt:bf:af","bt:ls:af","rs:bf:ls","rs:bf:af","rs:ls:af","bf:ls:af","bt:rs:bf:ls","bt:rs:bf:af","bt:rs:ls:af","bt:bf:ls:af","rs:bf:ls:af","bt:rs:bf:ls:af","in","ou","in:ou"]

    def __init__(self):
        self.inColumnInit()
        self.ouColumnInit()

    def get_value(self,rowKey, columnKey):
        if columnKey == "in":
            return self.__inColumn[self.__rowList.index(rowKey)]    
        else:
            return self.__ouColumn[self.__rowList.index(rowKey)]


    def ouColumnInit(self):
        #ProjectiveRelation("rs:ls").augment(ProjectiveRelation().add_rel_from_CSR("bt,bf").delta())
        self.__ouColumn.append(DD)
        self.__ouColumn.append(DD)
        self.__ouColumn.append(DD)
        self.__ouColumn.append(DD) 
        self.__inColumn.append(ProjectiveRelation("IMP")) #RIGA DA DECOMMENTARE APPENA VIENE INSERITA IMP
        #self.__ouColumn.append(DC) #ATTENZIONE: INSERITA SOLO ALLO SCOPO DI TEST. APPENA VIENE INSERITA IMP, DECOMMENTARE LA RIGA SOPRASTANTE E CANCELLARE QUESTA
        for i in range(0,26):
            self.__ouColumn.append(DD)
        self.__ouColumn.append(DC)
        self.__ouColumn.append(DC)
        self.__ouColumn.append(DC)


    def inColumnInit(self):
        #ProjectiveRelation("rs:ls").augment(ProjectiveRelation().add_rel_from_CSR("bt,bf").delta())
        self.__inColumn.append(ProjectiveRelation("bt"))
        self.__inColumn.append(ProjectiveRelation().add_rel_from_CSR("bt,rs,bf").delta())
        self.__inColumn.append(ProjectiveRelation().add_rel_from_CSR("bt,bf").delta())
        self.__inColumn.append(ProjectiveRelation().add_rel_from_CSR("bt,bf,ls").delta())
        self.__inColumn.append(ProjectiveRelation("IMP")) #RIGA DA DECOMMENTARE APPENA VIENE INSERITA IMP
        #self.__inColumn.append(DC)  #ATTENZIONE: INSERITA SOLO ALLO SCOPO DI TEST. APPENA VIENE INSERITA IMP, DECOMMENTARE LA RIGA SOPRASTANTE E CANCELLARE QUESTA
        self.__inColumn.append(ProjectiveRelation().add_rel_from_CSR("bt,rs,bf,af").delta())
        self.__inColumn.append(DD)
        self.__inColumn.append(ProjectiveRelation().add_rel_from_CSR("bt,bf,ls,af").delta())
        self.__inColumn.append(DD)
        self.__inColumn.append(ProjectiveRelation().add_rel_from_CSR("bt,rs,bf").delta())
        self.__inColumn.append(DD)
        self.__inColumn.append(DD)
        self.__inColumn.append(ProjectiveRelation().add_rel_from_CSR("bt,bf,ls").delta())

        for i in range(0,18):
            self.__inColumn.append(DD)
        self.__inColumn.append(ProjectiveRelation("in"))
        self.__inColumn.append(DC)
        self.__inColumn.append(DC)


class Table5_composition:
    __table = None

    def readTable(self):
        fileName = os.path.join(os.path.dirname(os.path.dirname(__file__)),"data","tableWithDeltasExpanded.pickle")
        with open(fileName, 'rb') as f:
            return pickle.load(f)

    def get_value(self, rowKey, subRowKey, columnKey):
        try:
            if self.__table == None:
                self.__table = self.readTable()
        except:
            print("Unable to load table.\n")
            exit()

        try:
            columnList = ['bt', 'rs', 'bf', 'ls', 'af']
            subRowsList = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
            if columnKey=="in" or columnKey=="ou":
                Table4=Table4_in_ou_columns()
                return Table4.get_value(rowKey,columnKey)
            else:
                return self.__table[str(rowKey)][subRowsList.index(subRowKey)][columnList.index(columnKey)]
        except:
                print("GetVALUE",rowKey,subRowKey,columnKey)
                print("Errore nella Table5_composition", sys.exc_info())
                return None

    def get_subrows(self, rowKey):
        if self.__table==None:
            self.__table = self.readTable()
        return self.__table[str(rowKey)][:][:]

    def get_ProjectiveRelation_object(self, rowKey, subRowKey, columnKey):
        value = self.get_value(rowKey, subRowKey, columnKey)
        returning_rel = ProjectiveRelation()
        for r in value:
            returning_rel.add_rel(r)

        return returning_rel





# now it is possible to initialize global variables
_set_global_values()
TABLE4=Table4_in_ou_columns()
TABLE5=Table5_composition()

'''
r=ProjectiveRelation("bf:ls")
q=ProjectiveRelation(RS)
print(r,"°", q, "=", _Operations.composition(r,q))
r=ProjectiveRelation("bf")
q=ProjectiveRelation(RS)
print(r,"°", q, "=", _Operations.composition(r,q))
r=ProjectiveRelation("rs")
q=ProjectiveRelation("bt:ls")
print(r,"°", q, "=", _Operations.composition(r,q))
r=ProjectiveRelation("rs:ls")
q=ProjectiveRelation("bt:rs:bf")
print(r,"°", q, "=", _Operations.composition(r,q))
r=ProjectiveRelation("rs")
q=ProjectiveRelation("bt:rs:ls")
print(r,"°", q, "=", _Operations.composition(r,q))
'''
