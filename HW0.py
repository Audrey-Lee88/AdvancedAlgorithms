
def initialTableau(c, A, b):
    # each row of A with b tacked on
    tableau = [row[:] + [x] for row, x in zip(A, b)]
    # make the max func the same size
    tableau.append(c[:] + [0,0,0,0])
    # print(tableau)
    return tableau


def canImprove(tableau):
    # if any of the vals in the last row are positive, it can improve
    lastRow = tableau[-1]
    return any(x > 0 for x in lastRow[:-1])


def findPivotIndex(tableau):
    # import pdb
    # pdb.set_trace()
    # pick first nonzero index of the last row
    column = [i for i, x in enumerate(tableau[-1][:-1]) if x > 0][0]
    # calculate the ratios
    ratios = [(i, r[-1] / r[column]) for i, r in enumerate(tableau[:-1]) if r[column] > 0]
    # ratios = []
    # for i, r in enumerate(tableau[:-1]):
    #     if r[column] != 0:
    #         ratios.append((i, r[-1] / r[column]))
    #         # print(r, r[-1], r[column])
    # print("ratios:",ratios)

    # pick row index minimizing the ratio
    row = min(ratios, key=lambda x: x[1])[0]
    # print("row:", row)
    return row, column


def pivotAbout(tableau, pivot):
    """  Divide the pivot row by the value of the pivot entry.
    Then use the pivot row to zero out all entries in the pivot
    column above and below the pivot entry"""
    i, j = pivot

    pivotDenom = tableau[i][j]
    tableau[i] = [x / pivotDenom for x in tableau[i]]

    for k, row in enumerate(tableau):
        if k != i:
            pivotRow = [y * tableau[k][j] for y in tableau[i]]
            tableau[k] = [(x - y) for x, y in zip(tableau[k], pivotRow)]


def transpose(tableau):
    # transpose the matrix
    return list(zip(*tableau))


def primalSolution(tableau):
    # the pivot columns denote which variables are used
    columns = transpose(tableau)
    indices = [j for j, col in enumerate(columns[:-1]) if sum(col) == 1]
    return list(zip(indices, columns[-1]))


def objectiveValue(tableau):
    # Last entry is maximum soln
    return -(tableau[-1][-1])


def simplex(c, A, b):
    # make it into a tableau
    tableau = initialTableau(c, A, b)

    while canImprove(tableau):
        pivot = findPivotIndex(tableau)
        print("pivot:", pivot)
        pivotAbout(tableau, pivot)
    # print(tableau)
    return primalSolution(tableau), objectiveValue(tableau)


if __name__ == "__main__":
    c = [8,-6,4]
    A = [[1,1,1,1,0,0],[5,3,0,0,1,0],[0,9,2,0,0,1]]
    b = [12,20,15]
    print(simplex(c,A,b))