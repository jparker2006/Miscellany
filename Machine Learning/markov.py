import random, sys

def dot(v, m): # vector dot matrice
    new_vector = []
    for x in range(1): # 1 would usually be len(m2), since vector, only need 1 iteration
        for y in range(len(m[0])):
            current_sum = 0;
            for z in range(len(v)):
                current_sum += v[z] * m[z][y];
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
    #sDirectory = sys.argv[1]
    sDirectory = "/Users/jparker/Desktop/sonnets.txt"
    sFile = open(sDirectory, "r+").read()
    stocm = stochastic_matrix(sFile)


    probv = []
    for i in range(256):
        probv.append(0)
    nRand = random.randint(65, 90) # random uppercase letter
    probv[nRand] += 1
    #sName = chr(nRand)
    #current_char = sName

    for i in range(100):
        past_probv = probv
        probv = dot_product(probv, stocm)
        if past_probv == probv:
            #print("stationary state after " + str(i) + " iterations")
            break
    print(probv)
    return

    """
    for i in range(100):
        max_value = max(probv[0])
        max_index = probv[0].index(max_value)
        if ('\n' == chr(max_index)):
            print("BREAKING OUT")
            return
            probv = [ [] ]
            for j in range(256):
                probv[0].append(0)
            probv[0][random.randint(65, 90)] += 1
        else:
            print(current_char)
            probv[0][ord(current_char)] = 0
            current_char = chr(max_index)
            sName += current_char
            probv[0][ord(current_char)] = 1
            for j in range(100):
                past_probv = probv
                probv = dot_product(probv, stocm)
                if past_probv == probv:
                    #print("stationary state after " + str(i) + " iterations")
                    break

    # put the probv vectors probabilities into the walk function and generate based when you get to the eigenvector
    probv = [ [] ]
    for i in range(256):
        probv[0].append(0)

    probv[0][random.randint(65, 90)] += 1

    for i in range(250):
        past_probv = probv
        probv = dot_product(probv, stocm)
        if past_probv == probv:
            print("stationary state after " + str(i) + " iterations")
            break

    """

if "__main__" == __name__:
    main()

