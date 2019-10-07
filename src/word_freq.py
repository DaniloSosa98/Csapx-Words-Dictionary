import csv
import argparse
import sys
from operator import attrgetter
from collections import namedtuple
import matplotlib.pyplot as plt


ERR = sys.stderr.write
Word = namedtuple('Word', ('name', 'occur'))
wordsL = list()
def read_words(filename: str) -> dict:
    Wdict = {}
    Wdict = dict()

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, skipinitialspace=True)
        for line in csv_reader:
            if line[0] in Wdict:
                Wdict[line[0]].get('years').append(line[1])
                Wdict[line[0]].get('occur').append(line[2])
            else:
                Wdict[line[0]] = {'years': [line[1]], 'occur': [line[2]]}

    return Wdict

def word_occur(Dtotal: dict, find:str) -> dict:
    for word in Dtotal:
        count = 0
        for element in Dtotal[word].get('occur'):
            count += int(element)
        Dtotal[word] = {'total': count}

        wordsL.append(Word(name = word, occur = count))

    return Dtotal

def order(Dtotal: dict) -> list :

    return sorted(wordsL, key=attrgetter('occur'), reverse = True)

def Lranks(max: int):

    if max <= len(wordsL):
        for i in range(max):
            print('#{}: {} -> {}'.format(i+1, wordsL[i].name, wordsL[i].occur))
    else:
        ERR('Index outside of range\n\n')

def findW(wordsL: list, find: str, filename: str) -> int:

    rank = 0
    while rank < len(wordsL) and wordsL[rank].name != find:
        rank += 1
    if rank < len(wordsL):
        print('{} is ranked #{}'.format(find, rank + 1))
        return rank+1
    else:
        ERR('Error: president does not appear in {}\n\n'.format(filename))

    return rank + 1

def plotL(wordsL: list, keyL:list, valueL:list):

    for i in range(len(wordsL)):
        keyL.append(i+1)
        valueL.append(wordsL[i].occur)

def main() -> None:

    global find, wordsL, keyL, valueL, Wrank, Wdict, Wocur
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--output", type=int, help="display the top OUTPUT (#) ranked words by "
                                                                   "number of occurrences")
    parser.add_argument("-p","--plot", action="store_true", help="plot letter frequencies using matplotlib")
    parser.add_argument("word", help="a word to display the overall ranking of")
    parser.add_argument("filename", help="a comma separated value unigram file")
    args = parser.parse_args()
    filename = ('../' + args.filename)

    if filename[-4:] != '.csv':
        ERR('Error: {} does not exist!\n\n'.format(args.filename))
    else:
        Wocur  = 0
        keyL = []
        valueL = []
        find = args.word
        Wdict = read_words(filename)
        Wdict = word_occur(Wdict, find)
        wordsL = order(Wdict)

    if args.word:
        Wrank = findW(wordsL, find, args.filename)
    if args.output:
        Lranks(args.output)
    if args.plot:
        plotL(wordsL, keyL, valueL)
        plt.plot(keyL, valueL, 'k-o')
        plt.xscale("log")
        plt.yscale("log")
        plt.title('Word Frequencies: {}'.format(args.filename))
        plt.xlabel('Rank of word ("{}" is rank {})'.format(find, Wrank))
        plt.ylabel('Total number of occurrences')
        plt.text(Wrank,Wdict[find].get('total'),'{}'.format(find))
        plt.show()


if __name__ == '__main__':
    main()