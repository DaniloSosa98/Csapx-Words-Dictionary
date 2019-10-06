import csv
import argparse
import sys
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
                Wdict[line[0]].get('length').append(len(line[0])*int(line[2]))
                Wdict[line[0]].get('total').append(int(line[2]))
            else:
                Wdict[line[0]] = {'years': [line[1]], 'length': [len(line[0])*int(line[2])], 'total': [int(line[2])]}
    return Wdict

def store(Wdict: dict) ->dict:
    Adict = {}
    Adict = dict()
    for element in Wdict:
        i = 0
        for year in  Wdict.get(element)['years']:
            if year in Adict:
                Adict[year].get('length').append(Wdict.get(element)['length'][i])
                Adict[year].get('total').append(Wdict.get(element)['total'][i])
                i += 1
            else:
                Adict[year] = {'length': [Wdict.get(element)['length'][i]], 'total': [Wdict.get(element)['total'][i]]}
                i += 1
    return Adict

def avrg(Wdict:dict):
    Fdict = {}
    Fdict  = dict()
    for element in Wdict:
        lengths = Wdict[element].get('length')
        sums = Wdict[element].get('total')
        Wdict[element] = {'average':sum(lengths)/sum(sums)}

    return Wdict

def printL(Wdict:dict, start:str, end:str):
    i = 0
    while i <= int(end) - int(start):
        current = str( int(start) + i )
        print( '{}: {}'.format(current, Wdict[current]['average']) )
        i += 1


def main() -> None:

    global find, wordsL, Wdict
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--output", action="store_true", help="display the average word lengths over years")
    parser.add_argument("-p","--plot", action="store_true", help="plot the average word lengths over years")
    parser.add_argument("start", help="the starting year range")
    parser.add_argument("end", help="the ending year range")
    parser.add_argument("filename", help="a comma separated value unigram file")
    args = parser.parse_args()
    filename = ('../' + args.filename)

    if filename[-4:] != '.csv':
        ERR('Error: {} does not exist!\n\n'.format(args.filename))
    else:
        Wdict = read_words(filename)
        Wdict = store(Wdict)
        Wdict = avrg(Wdict)

    if args.output:
        start = args.start
        end = args.end
        if start > end:
            ERR('Error: start year must be less than or equal to end year!\n\n')
        else:
            printL(Wdict, start, end)

    if args.plot:
        print('plot')

if __name__ == '__main__':
    main()