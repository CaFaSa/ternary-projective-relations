from Model.Relations import *
from Model.Relations import _SingleProjectiveRelation


#Test di base
def run_test_1():
    print("creo una basic relation: in,ou,af,ls,rs")
    a = _SingleProjectiveRelation(IN, OU, AF, LS, RS)
    print(a)

    print()
    print("creo una basic relation: in,rs,ls")
    b = _SingleProjectiveRelation()
    b.add_rel(IN, RS, LS)
    print(b)

    print()
    print("creo una multi tile relation tra le due basic relation precedenti: ", a, b)
    c = _SingleProjectiveRelation(IN, RS)
    multi = ProjectiveRelation(a, b)
    print(multi)

    print()
    print("faccio il get dell'insieme della prima basic relation e della multi tile relation")
    print(a.get_relations())
    print(multi.get_relations())
    # print(multi.get_relations().pop().get_relations())

    print()
    print("elimino in e ou dalla prima relazione")
    print(a)
    a.remove_relations("in", "ou")
    print(a)

    print()
    print("calcolo la converse della relazione: ", a)
    print(a.converse())
    print(a.converse().get_relations())

    print()
    print("aggiungo una rel a multi")
    multi.add_rel(a, b, c)
    print(a)
    print(b)
    print(multi)

    # print()
    # print("calcolo delta(", a, ")")
    # _Operations.delta(a)


# add_rel test
def run_test_2():
    a = _SingleProjectiveRelation(AF, LS, RS)

    b = _SingleProjectiveRelation()
    b.add_rel(RS, BF)

    multi = ProjectiveRelation()
    multi.add_rel(a)
    multi.add_rel(b)
    print(multi)
    multi.converse()

# add_rel_from_string test
def run_test_3():
    a = _SingleProjectiveRelation()
    a.add_rel(IN)
    a.add_rel(OU, IN, BT)
    a.add_rel_from_str("rs")

    b = ProjectiveRelation()
    b.add_rel(a, a)

    b._add_rel_from_str("bf")
    b._add_rel_from_str("bf:af")

    print(b)

# _add_rel_from_str with  multi-tile-relations strings
def run_test_4():
    a = ProjectiveRelation()
    a._add_rel_from_str("ls:bf:af")
    a.add_rel(LS)
    a.add_rel("ls:rs")
    print(a)

# Table5_composition access test
def run_test_5():
    a = Table5_composition()
    b = a.get_value("bt:rs", "a", "af")

    print(type(a.get_ProjectiveRelation_object("bt:rs", "a", "af")))

# iterator test for _SingleProjectiveRelation
def run_test_6():
    b = _SingleProjectiveRelation()
    b.add_rel(LS)
    b.add_rel(BF)
    print(b)
    print(b.get_relations())

    for i in b:
        print(i)

    print(b)

# iterator test for ProjectiveRelation
def run_test_7():
    a = ProjectiveRelation()
    a.add_rel("bf:ls:rs")
    a.add_rel("ls:bf")

    i = 1
    for r in a:
        print(i, "--", r)
        i = i + 1

    print(a)

# testing delta function for single projective relation
def run_test_8():
    a = _SingleProjectiveRelation()
    a.add_rel(LS, BF)
    print(a.delta())

    a = _SingleProjectiveRelation()
    a.add_rel(LS, BF, OU)
    print("bf:ls:ou, bf, bf:ou, ou, ls, bf:ls, ls:ou EXPECTED")
    print(a.delta())

# testing delta function for BasicProjectiveRelation
def run_test_9():
    a = ProjectiveRelation()
    a.add_rel("bf:ls:rs")
    a.add_rel("bf:af")
    print(a.delta())

# Testing product function
def run_test_10():
    a = ProjectiveRelation()
    a.add_rel("bt")
    a.add_rel("rs")
    b = ProjectiveRelation()
    b.add_rel("bf")
    b.add_rel("ls")

    print(a, " PRODUCT ", b, "=", a.product(b))

    c = ProjectiveRelation()
    d = ProjectiveRelation()
    e = ProjectiveRelation()
    c.add_rel("rs:ls")
    c.add_rel("bt")
    d.add_rel("bt:rs:ls")
    d.add_rel("rs:bf:ls")
    e.add_rel("bf")

    print()
    print("rs:bf:ls, bt:rs:bf:ls EXPECTED")
    print((c.product(d).product(e)))

    expected = ProjectiveRelation().add_rel("bt:rs:bf:ls").add_rel("rs:bf:ls")
    print(expected)

    if c.product(d).product(e) != expected:
        raise ValueError("TEST 10 FAILED")

# Testing augment operator (also called as "/" in Clementini's notation)
def run_test_11():
    a = ProjectiveRelation()
    a.add_rel("rs:ls")
    b = ProjectiveRelation()
    b.add_rel("bt").add_rel("bf")

    expected = ProjectiveRelation().add_rel("rs:ls").add_rel("bt:rs:ls").add_rel("rs:bf:ls").add_rel("bt:rs:bf:ls")

    a.augment(b.delta())

    print(expected, "EXPECTED")
    print(a.augment(b.delta()))

    if expected != a.augment(b.delta()):
        print("------", expected, "EXPECTED")
        print("------", a.augment(b.delta()))
        raise ValueError("TEST 11 FAILED")

# Testing add_from_CSR method
def run_test_12():
    a = ProjectiveRelation()
    a.add_rel_from_CSR("bf:rs,bf,rs:in,IN:Ou,ls,  bf:ls")

    expected = ProjectiveRelation().add_rel("bf:rs").add_rel("bf").add_rel("rs:in").add_rel("in:ou").add_rel("ls").add_rel("bf:ls")

    print(expected, "EXPECED")
    print(a)

    if expected != a:
        raise ValueError("TEST 12 FAILED")

#testing equality operator (implicitely also sorting algorythm)
#this also tests table reading
def run_test_13():
    A = Table5_composition()
    B = Table5_composition()

    for i in range(1000):
        a = A.get_ProjectiveRelation_object("rs", "a", "ls")
        b = B.get_ProjectiveRelation_object("rs", "a", "ls")
        c = ProjectiveRelation().add_rel_from_CSR("rs,bf,bf:rs")

        if (not(a==b and a==c)):
            print(a == c)
            print("A:", a)
            print("C", c)
            raise ValueError("TEST 13 FAILED")

# Testing projective relation constructor while passing multiple ProjectiveRelation objects
def run_test_14():
    a1 = ProjectiveRelation("rs")
    a2 = ProjectiveRelation("bf")
    a3 = ProjectiveRelation(a1, a2, ProjectiveRelation("bf"), ProjectiveRelation().add_rel_from_CSR("bf:rs, bf, rs"))
    expected = ProjectiveRelation().add_rel_from_CSR("rs, bf, rs:bf")

    if expected != a3:
        raise ValueError("TEST 14 FAILED")

# Testing rotate operator
def run_test_15():
    a = ProjectiveRelation("rs, bt:rs:ls:af:bf")
    expected = ProjectiveRelation("rs, in, ou, in:ou")

    if expected != a.rotate():
        raise ValueError("TEST 15 FAILED")


#intersection union and composition test...
def run_test_16():
    a=ProjectiveRelation("ls:bf,ls")
    b=ProjectiveRelation("ls:bf, rs")
    c= a.union(b)
    d=a.intersection(b)
    e=a.composition(b)
    expected_c = ProjectiveRelation("rs, ls, bf:ls")
    expected_d = ProjectiveRelation("bf:ls")
    expected_e = ProjectiveRelation("ls, rs:bf, bt:ls:af, rs:bf:ls, rs:bf:af, bt:bf:ls:af")
    if expected_c != c:
        raise ValueError("TEST 16-c FAILED")
    if expected_d != d:
        raise ValueError("TEST 16-d FAILED")
    if expected_e != e:
        raise ValueError("TEST 16-e FAILED")


#TODO: To complete composition in-ou rule test
def run_test_17():
    a=ProjectiveRelation("ls:bf,ls")
    b=ProjectiveRelation("in:ou")
    e=a.composition(b)


#imp and empty string insertion test
def run_test_18():
    a = ProjectiveRelation("imp, ls, IMP, "", bf,rs")
    expected = "rs, bf, ls"

    if expected != str(a):
        raise ValueError("TEST 17- FAILED")


if __name__ == '__main__':
    try:
        run_test_1()
        run_test_2()
        run_test_3()
        run_test_4()
        run_test_5()
        run_test_6()
        run_test_7()
        run_test_8()
        run_test_9()
        run_test_10()
        run_test_11()
        run_test_12()
        run_test_13()
        run_test_14()
        run_test_15()
        run_test_16()
        run_test_17()
        run_test_18()

        print("SUCCESS!")
    except Exception as e:
        print("Test failed:", e)

