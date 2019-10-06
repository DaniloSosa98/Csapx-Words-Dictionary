import csv
import argparse
import sys
from operator import attrgetter
from collections import namedtuple

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

def word_occur(Dtotal: dict) -> dict:
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

def findW(wordsL: list, find: str, filename: str):

    rank = 0
    while rank < len(wordsL) and wordsL[rank].name != find:
        rank += 1
    if rank < len(wordsL):
        print('{} is ranked #{}'.format(find, rank + 1))
    else:
        ERR('Error: president does not appear in {}\n\n'.format(filename))

def main() -> None:

    global find, wordsL
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
        Wdict = read_words(filename)
        Wdict = word_occur(Wdict)
        wordsL = order(Wdict)
        find = args.word
    if args.word:
        findW(wordsL, find, args.filename)
    if args.output:
        Lranks(args.output)
    if args.plot:
        print('plot')

if __name__ == '__main__':
    main()