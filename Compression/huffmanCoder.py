import time, sys

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, data):
        self.queue.append(data)

    def pop(self):
        imax = 0
        for i in range(len(self.queue)):
            if self.queue[i].nFrequency < self.queue[imax].nFrequency:
                imax = i
        del self.queue[imax]

    def root(self):
        imax = 0
        for i in range(len(self.queue)):
            if self.queue[i].nFrequency < self.queue[imax].nFrequency:
                imax = i
        return self.queue[imax]

    def size(self):
        return len(self.queue)

class Node:
    def __init__(self, nFrequency, cLetter):
        self.nFrequency = nFrequency
        self.cLetter = cLetter
        self.left = None
        self.right = None

    def traverse(self, sCode, dLegend):
        if None != self.left:
            self.left.traverse(sCode + "0", dLegend)
            self.right.traverse(sCode + "1", dLegend)
        else:
            if self.cLetter:
                dLegend[self.cLetter] = sCode
        return dLegend

def readFileToString(sDirectory):
    sUncompressed = open(sDirectory, "r+").read()
    print("# of bits uncompressed: " + str(len(sUncompressed) * 8))
    return sUncompressed.strip()

def makeFrequencyMap(sUncompressed):
    aFrequencies = []
    for i in range(256):
        aFrequencies.append(0)
    for i in range(len(sUncompressed)):
        aFrequencies[ord(sUncompressed[i])] += 1
    return aFrequencies

def makePriorityQueue(aFrequencies):
    queue = PriorityQueue()
    for i in range(256):
        if 0 != aFrequencies[i]:
            queue.push(Node(aFrequencies[i], chr(i)))
    return queue

def makeHuffmanCode(pQueue):
    while pQueue.size() > 1:
        cdrnLft = pQueue.root()
        pQueue.pop()
        cdrnRgt = pQueue.root()
        pQueue.pop()
        newNode = Node(cdrnLft.nFrequency + cdrnRgt.nFrequency, None)
        newNode.left = cdrnLft
        newNode.right = cdrnRgt
        pQueue.push(newNode)
    return pQueue.root()

def calculateCompressionRatio(nUncompressedBits, nCompressedBits):
    print("# of bits compressed: " + str(nCompressedBits))
    fCompressionRatio = nCompressedBits / float(nUncompressedBits)
    print("Compressed file is " + str(round(fCompressionRatio * 100, 3)) + "% of the original")

def getBinaryData(sUncompressed, dLegend):
    sBinary = ""
    nCompressedBits = 0
    for i in range(len(sUncompressed)):
        sBinary += dLegend[sUncompressed[i]]
        nCompressedBits += len(dLegend[sUncompressed[i]])
    return (sBinary, nCompressedBits)

def compress(sFileDirectory):
    sUncompressed = readFileToString(sFileDirectory)
    nUncompressedBits = len(sUncompressed * 8)
    aFrequencies = makeFrequencyMap(sUncompressed)
    pQueue = makePriorityQueue(aFrequencies)
    root = makeHuffmanCode(pQueue)
    dLegend = root.traverse("", {})
    binaryData = getBinaryData(sUncompressed, dLegend)
    calculateCompressionRatio(nUncompressedBits, binaryData[1])
    return (binaryData[0], root, dLegend)

def decompress(sCompressed, root):
    sUncompressed = ""
    curr = root
    for i in range(len(sCompressed)):
        if '0' == sCompressed[i]:
            curr = curr.left
        else:
            curr = curr.right

        if None == curr.left and None == curr.right:
            sUncompressed += curr.cLetter
            curr = root
    return sUncompressed

def main():
    fStart = time.time()
    tCompressed = compress(sys.argv[1])
    print("Compression completed in " + str(round((time.time() - fStart) * 1000, 4)) + "ms")
    fStart = time.time()
    sDecompressed = decompress(tCompressed[0], tCompressed[1])
    print("Decompression completed in " + str(round((time.time() - fStart) * 1000, 4)) + "ms")

if "__main__" == __name__:
    main()
