def testIfAdjacent(white, black, a):
    set1 = []
    set2 = []
    set3 = []
    set4 = []
    m = 1
    while m <= 5:
        set1.append(5 * m - 4)
        set2.append(5 * m)
        set3.append(m)
        set4.append(m + 20)
        m += 1
    x = []
    z = []
    if white[a] - 1 in black and white[a] not in set1:
        x.append(white[a])
        z.append(1)
    if white[a] + 1 in black and white[a] not in set2:
        x.append(white[a])
        z.append(2)
    if white[a] - 5 in black and white[a] not in set3:
        x.append(white[a])
        z.append(3)
    if white[a] + 5 in black and white[a] not in set4:
        x.append(white[a])
        z.append(4)
    if len(x) == 4 or len(x) == 0:
        pass
    else:
        return [a, z]


def testIfMoveTo(white, black):
    a = 0
    set1 = []
    set2 = []
    set3 = []
    set4 = []
    m = 1
    while m <= 5:
        set1.append(5 * m - 3)
        set2.append(5 * m - 1)
        set3.append(m + 5)
        set4.append(m + 15)
        m += 1
    while a < len(white):
        x = []
        y = []
        z = []
        if (
            white[a] - 1 not in white and white[a] - 1 not in black and
                white[a] and white[a] - 1 in range(1, 26)
        ):
            white[a] -= 1
            y.append(testIfAdjacent(white, black, a))
            z.append(1)
            if y[0] is not None and y[0][0] != a:
                y[0] = None
                z[0] = 0
            white[a] += 1
        else:
            y.append(None)
            z.append(0)
        if (
            white[a] + 1 not in white and white[a] + 1 not in black and
                white[a] and white[a] + 1 in range(1, 26)
        ):
            white[a] += 1
            y.append(testIfAdjacent(white, black, a))
            z.append(2)
            if y[1] is not None and y[1][0] != a:
                y[1] = None
                z[1] = 0
            white[a] -= 1
        else:
            y.append(None)
            z.append(0)
        if (
            white[a] - 5 not in white and white[a] - 5 not in black and
                white[a] and white[a] - 5 in range(1, 26)
        ):
            white[a] -= 5
            y.append(testIfAdjacent(white, black, a))
            z.append(3)
            if y[2] is not None and y[2][0] != a:
                y[2] = None
                z[2] = 0
            white[a] += 5
        else:
            y.append(None)
            z.append(0)
        if (
            white[a] + 5 not in white and white[a] + 5 not in black and
                white[a] and white[a] + 5 in range(1, 26)
        ):
            white[a] += 5
            y.append(testIfAdjacent(white, black, a))
            z.append(4)
            if y[3] is not None and y[3][0] != a:
                y[3] = None
                z[3] = 0
            white[a] -= 5
        else:
            y.append(None)
            z.append(0)
        b = 0
        while b < len(y):
            if y[b] is None:
                z[b] = 0
            else:
                x.append(y[b])
            b += 1
        t = []
        c = 0
        while c < len(z):
            if z[c] != 0:
                t.append(z[c])
            c += 1
        if len(t) != 0:
            return [a, t]
        a += 1


def main():
    a = 0
    set1 = []
    m = 1
    while m <= 5:
        set1.append(5 * m - 4)
        set1.append(5 * m)
        set1.append(m)
        set1.append(m + 20)
        m += 1
    while a < 5:
        x = input()
        numOfWhite = x[0]
        white = list(x[1:numOfWhite + 1])
        black = list(x[numOfWhite + 2:])
        b = 0
        adjacent = []
        while b < numOfWhite:
            y = testIfAdjacent(white, black, b)
            if y is not None:
                adjacent.append(y)
            b += 1
        len1 = -1
        try:
            len1 = len(adjacent)
        except:
            pass
        if len1 == 0 or len1 == -1:
            moveTo = testIfMoveTo(white, black)
            setOfMovement = [-1, 1, -5, 5]
            if moveTo is not None:
                white[moveTo[0]] += setOfMovement[moveTo[1][0] - 1]
                adjacent = list(adjacent)
                adjacent = [testIfAdjacent(white, black, moveTo[0])]
                movement = adjacent[0][1][0]
                setOfMovement = [-1, 1, -5, 5]
                endUp = white[adjacent[0][0]] + setOfMovement[movement - 1]
                n = [0, 0, 0, 0]
                c = movement - 1
                if (
                    endUp + setOfMovement[c] in black and endUp +
                        setOfMovement[c] in set1
                ):
                    if (
                        endUp + 2 * setOfMovement[c] in black and endUp + 2 *
                            setOfMovement[c] in set1
                    ):
                        if (
                            endUp + 3 * setOfMovement[c] in black and endUp + 3
                                * setOfMovement[c] in set1
                        ):
                            if (
                                endUp + 4 * setOfMovement[c] in black and endUp
                                    + 4 * setOfMovement[c] in set1
                            ):
                                n[c] = 4
                            else:
                                n[c] = 3
                        else:
                            n[c] = 2
                    else:
                        n[c] = 1
                else:
                    n[c] = 0
                d = 0
                while d < 4:
                    if (
                        n[d] >= n[0] and n[d] >= n[1] and n[d] >= n[2] and n[d]
                            >= n[3]
                    ):
                        z = d
                    d += 1
                chainMovement = setOfMovement[z]
                startChain = endUp
                setToBeCaptured = []
                e = 0
                while e < 5:
                    possibleList = startChain + e * chainMovement
                    if (
                        possibleList <= 25 and possibleList > 0 and
                            possibleList in black
                    ):
                        setToBeCaptured.append(startChain + e * chainMovement)
                    else:
                        break
                    e += 1
                setToBeCaptured.sort()
                f = 0
                g = ""
                while f < len(setToBeCaptured) - 1:
                    g += str(setToBeCaptured[f])
                    g += ", "
                    f += 1
                g += str(setToBeCaptured[f])
                print g
            else:
                print "NONE"
        else:
            adjacent = list(adjacent)
            movement = adjacent[0][1][0]
            setOfMovement = [-1, 1, -5, 5]
            endUp = white[adjacent[0][0]] + setOfMovement[movement - 1]
            c = 0
            n = [0, 0, 0, 0]
            c = movement - 1
            if (
                endUp + setOfMovement[c] in black and endUp + setOfMovement[c]
                    in set1
            ):
                if (
                    endUp + 2 * setOfMovement[c] in black and endUp + 2 *
                        setOfMovement[c] in set1
                ):
                    if (
                        endUp + 3 * setOfMovement[c] in black and endUp + 3 *
                            setOfMovement[c] in set1
                    ):
                        if (
                            endUp + 4 * setOfMovement[c] in black and endUp + 4
                                * setOfMovement[c] in set1
                        ):
                            n[c] = 4
                        else:
                            n[c] = 3
                    else:
                        n[c] = 2
                else:
                    n[c] = 1
            else:
                n[c] = 0
            d = 0
            while d < 4:
                if (
                    n[d] >= n[0] and n[d] >= n[1] and n[d] >= n[2] and n[d] >=
                        n[3]
                ):
                    z = d
                d += 1
            chainMovement = setOfMovement[z]
            startChain = endUp
            setToBeCaptured = []
            e = 0
            while e < 5:
                possibleList = startChain + e * chainMovement
                if (
                    possibleList <= 25 and possibleList > 0 and possibleList in
                        black
                ):
                    setToBeCaptured.append(possibleList)
                else:
                    break
                e += 1
            if len(setToBeCaptured) == 0:
                print "NONE"
            else:
                setToBeCaptured.sort()
                f = 0
                g = ""
                while f < len(setToBeCaptured) - 1:
                    g += str(setToBeCaptured[f])
                    g += ", "
                    f += 1
                g += str(setToBeCaptured[f])
                print g
        a += 1

main()
