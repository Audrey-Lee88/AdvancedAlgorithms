import random
import pytest


def find_pure_vars(cnf):
    """Finds all pure literals in a list of clauses."""
    seen_vars = [var for clause in cnf for var in clause]
    return [var for var in seen_vars if (var[0],False) not in seen_vars]


def find_unit_clause(cnf):
    """ Finds the unit clauses in a list of clauses """
    return [clause for clause in cnf if len(clause) == 1]


def select_literal(cnf):
    """
    Given a cnf, pick a literal
    """
    for c in cnf:
        for literal in c:
            return literal[0]


def dpll(cnf):
    """
    Takes a set of clauses and returns a boolean

    """
    # if cnf is empty, return True
    if len(cnf) == 0:
        return True

    # if there exists an empty clause, return False
    if any([len(c) == 0 for c in cnf]):
        return False

    # if any pure literals, remove them
    if any(find_pure_vars(cnf)):
        cnf = [c for c in cnf if find_pure_vars(cnf)[0] not in c]
    # If any unit clauses, remove them
    if any(find_unit_clause(cnf)):
        cnf = [c for c in cnf if find_unit_clause(cnf)[0] not in c]
    # pick a literal from whatever is left
    l = select_literal(cnf)

    # get rid of every occurence of l and unit clause ~l in c
    new_cnf = [c for c in cnf if (l, True) not in c]
    new_cnf = [c.difference({(l, False)}) for c in new_cnf]
    if dpll(new_cnf):
        return True

    # get rid of every occurence of ~l and unit clause l in c
    new_cnf = [c for c in cnf if (l, False) not in c]
    new_cnf = [c.difference({(l, True)}) for c in new_cnf]
    if dpll(new_cnf):
        return True

    return False


def random_kcnf(n_lit, n_clause):
    """
    This was used for debugging

    Generate random cnf with n clause, random k literals per each clause,
    and picks a random literal to assign a random boolean value to

    Each literal is in the form of (l, T) or (l,F) where l is the literal and T/F is True/False
    Each clause is in the form of {(l,T),(l,F),...}
    Returns cnf in list format
    """
    cnf = []
    for _ in range(n_clause):
        k = random.randint(1, 5)
        conj = set()
        for _ in range(k):
            index = random.randint(0, n_lit)
            conj.add((
                index,
                bool(random.randint(0, 1)),
            ))
        cnf.append(conj)
    print(cnf,'result')
    return cnf


def test_dpll():
    # Testing problem 3 (3 Colorabiltiy cnf) which will return True
    c = [{(1, True), (2, True), (3, False)}, {(1, False), (2, False), (3, True)}, {(1, False), (2, True),(3, False)}]
    assert dpll(c) == True

    # Testing a case where it will return False
    c = [{(1, True), (2, False), (3, False)}, {(1, False)}, {(1, True)}]
    assert dpll(c) == False

    # Testing a case where there's a pure literal/unit clause
    c = [{(1, True), (2, False), (3, False)}, {(1, True)}]
    assert dpll(c) == True

    # Testing a case where there's just a unit clause
    c = [{(1, True), (2, False), (3, False)}, {(1, False)}]
    assert dpll(c) == True

    # Testing empty list
    c = []
    assert dpll(c) == True

    # Testing empty set
    c = [{}]
    assert dpll(c) == False


if __name__ == "__main__":
    c = [{(1, True), (2, False), (3, False)}, {(1, False)}, {(1, True)}]
    print(dpll(c))

    ### For debugging ###
    # for lit in range(3):
        # con = random.randint(0, lit * 6)
        # s = random_kcnf(lit, con)
        # print(dpll(s))
    # test_dpll()