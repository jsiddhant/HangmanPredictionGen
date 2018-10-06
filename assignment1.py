import operator
import string

def main():

    wordLength = int(input("Please enter the Length of Word (5-10): "))
    print(wordLength)

    if wordLength == 5:
        filepath = 'hw1_word_counts_05.txt'
    elif wordLength == 6:
        filepath =  'hw1_word_counts_06.txt'
    elif wordLength == 7:
        filepath =  'hw1_word_counts_07.txt'
    elif wordLength == 8:
        filepath =  'hw1_word_counts_08.txt'
    elif wordLength == 9:
        filepath =  'hw1_word_counts_09.txt'
    elif wordLength == 10:
        filepath =  'hw1_word_counts_10.txt'
    else:
        raise ValueError('Sorry invalid length')

    wordFreq = getWordFrequency(filepath)

    ## Sanity Check
    # printMostandLeastFrequent(wordFreq)

    game = Hangman()
    game.updateEvidence([])

    ######################################################################## Change Evidence Here
    # Last Row
    # game.updateEvidence([('U',[1]), ('E',[-1]), ('I',[-1]), ('O',[-1]), ('S',[-1]), ('A', [-1])])

    # game.updateEvidence([('D',[0]), ('I',[3])])

    # game.updateEvidence([('E', [-1]), ('O', [-1])])
    # R0
    #
    #
    #
    ##############################################################################################

    game.calculateWgivenE(wordFreq)
    game.nextBestGuess()

## Print 5 Most and Least Frequent Words

def printMostandLeastFrequent(wordFrequencies):

    ## Replace word count with frequency
    sortedWords = sorted(wordFrequencies.items(), key=operator.itemgetter(1))

    ## Least Popular Words
    print("Least Frequent Words")
    for x in range(0, 6):
        print(sortedWords[x])

    ## Most Popular Words
    print("Most Frequent Words")
    for x in range(1, 7):
        print(sortedWords[sortedWords.__len__() - x])

## Extract Frequency and Words from Word Count File

def getWordFrequency(filename):

    wordsFreq = {}

    with open(filename) as fp:
        line = fp.readline()
        cnt = 1
        totalFrequency = 0
        while line:
            wordsFreq[line.split(' ')[0]] = int(line.split(' ')[1])
            totalFrequency += int(line.split(' ')[1])
            line = fp.readline()
            cnt += 1

    print('Total Words Read: ' + str(cnt))
    print(totalFrequency)

    for x in wordsFreq:
        wordsFreq[x] = float(wordsFreq[x] / totalFrequency)

    return wordsFreq

def wordContains(word, i):
    if i in word:
        return 1
    else:
        return 0

## Class for the Game
class Hangman:

    def __init__(self):
        self.evidence = {}

    def updateEvidence(self, letterPosition):
        for i in letterPosition:
            self.evidence[i[0]]=i[1]

        print(self.evidence)

    def calculateWgivenE(self, wordFrequencies):
        self.wGivenE = {}
        ## Calculate-> P(W=w/E)=(P(E/W=w)*P(w)) / sum(P(E/W=w)*P(w))
        ## Calculate the denominator

        sumProbab=0

        for i in wordFrequencies.keys():
            sumProbab += self.matchEvidence(i) * wordFrequencies[i]

        print(sumProbab)

        if sumProbab == 0:
            raise ValueError('Something Went Wrong SumProbab is Zero')

        ## Calculate total Num/Den
        for i in wordFrequencies.keys():
            if self.matchEvidence(i)!=0:
                self.wGivenE[i] = self.matchEvidence(i)*wordFrequencies[i]/sumProbab


    def nextBestGuess(self):
        bestChances=0

        possibleGuesses = string.ascii_uppercase

        for i in self.evidence.keys():
            possibleGuesses = possibleGuesses.replace(i, '')

        for i in possibleGuesses:
            totalChanceI =0
            for j in self.wGivenE.keys():
                    totalChanceI += wordContains(j,i) * self.wGivenE[j]

            if bestChances<totalChanceI:
                bestChances=totalChanceI
                bestLetter=i

        print('The next best guess is: ' + bestLetter + ' with probability ' + str(bestChances))



    ## Method to check if word complies with evidence returns 0 or 1
    def matchEvidence(self, word):

        for i in self.evidence.keys():
            iPosInWord = [pos for pos, char in enumerate(word) if char == i]

            ## Master Rejection Condition
            if (len(iPosInWord)==0 and self.evidence[i][0]!=-1) or (len(iPosInWord)!=0 and self.evidence[i][0]==-1):
                return 0

            ## Suppelemtary Rejection condition for when the letters are not in the same place
            elif iPosInWord != self.evidence[i] and len(iPosInWord)!=0:
                return 0

        return 1


if __name__ == "__main__":
    main()


