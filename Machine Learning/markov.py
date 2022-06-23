import random, re, sys

class MarkovChain:
    def __init__(self, norder, nmax_gen):
        self.norder = norder
        self.nmax_gen = nmax_gen
        self.d_ngrams = {}
        self.abeginnings = []
    def feed_chain(self, words):
        for x in range(len(words)):
            stext = words[x]
            for i in range(len(stext) - self.norder):
                sgram = stext[i:i + self.norder]
                if 0 == i:
                    self.abeginnings.append(sgram)
                cnext = stext[i + self.norder]
                if sgram not in self.d_ngrams:
                    self.d_ngrams[sgram] = []
                self.d_ngrams[sgram].append(cnext)
    def gen_data(self):
        scurrent = random.choice(self.abeginnings)
        sresult = scurrent
        while len(sresult) < self.nmax_gen:
            if scurrent in self.d_ngrams:
                aposs_next = self.d_ngrams[scurrent]
                snext = random.choice(aposs_next)
                sresult += snext
                scurrent = sresult[len(sresult) - self.norder:len(sresult)]
            else:
                break
        return ' '.join(sresult.split('\n'))

def main():
    sDirectory = sys.argv[1]
    sFile = open(sDirectory, "r+").read()
    delimiters = ['\n', ' ', ',', '.', '?', '!', ':', '_', '-']
    words = re.split(''.join(delimiters), sFile)
    chain = MarkovChain(4, 400)
    chain.feed_chain(words)
    print('\n' + chain.gen_data() + '\n')


if "__main__" == __name__:
    main()
