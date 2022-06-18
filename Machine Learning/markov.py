import random, sys

def dot(v, m): # vector dot matrice
    # dot is usually a 3 loop operation.
    # vector dot matrice means we only need 2 loops.
    # this is because a vector is a 1 row matrice
    new_vector = []
    for x in range(len(m[0])):
        current_sum = 0;
        for y in range(len(v)):
            current_sum += v[y] * m[y][x];
        new_vector.append(current_sum);
    return new_vector

def stochastic_matrix(sFile):
    stocm = []
    for i in range(256):
        stocm.append([])
        for j in range(256):
            stocm[i].append(0)
    for i in range(0, len(sFile) - 1):
        stocm[ord(sFile[i])][ord(sFile[i + 1])] += 1
    for i in range(256):
        row_total = 0
        for j in range(256):
            row_total += stocm[i][j]
        if 0 == row_total:
            continue
        for j in range(256):
            stocm[i][j] /= float(row_total)
    return stocm

def main():
    sDirectory = sys.argv[1]
    sFile = open(sDirectory, "r+").read()
    sFile = "".join(sFile.splitlines())
    stocm = stochastic_matrix(sFile)
    probv = []
    for i in range(256):
        probv.append(0)
    nRand = random.randint(65, 90) # random uppercase letter
    probv[nRand] += 1
    sName = chr(nRand)
    stoc_index = nRand
    for i in range(5):
        for j in range(100):
            past_probv = probv
            probv = dot(probv, stocm)
            if past_probv == probv: # stationary state
                break
        aProbs = []
        for i in range(97, 122):
            roundedp = round(probv[i], 4) * 100
            if roundedp < 1: # less than 1% probability
                continue
            for j in range(int(round(roundedp))):
                aProbs.append(chr(i))
        if 0 == len(aProbs):
            aProbs.append(chr(random.randint(97, 122)))
        nNextLetter = random.randint(0, len(aProbs) - 1)
        cNextLetter = aProbs[nNextLetter]
        stoc_index = ord(cNextLetter)
        sName += cNextLetter
        probv = []
        for j in range(256):
            probv.append(0)
        probv[stoc_index] += 1
    print(sName)

if "__main__" == __name__:
    main()
