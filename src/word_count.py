import csv
import argparse
import sys

ERR = sys.stderr.write

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

def Wcount(Wdict: dict, word: str) -> None:
    count = 0
    if word in Wdict:
        for element in Wdict[word].get('occur'):
            count += int(element)
        print('{} : {}'.format(word, count))
    else:
        ERR('Error: {} does not appear!\n\n'.format(word))

def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("word", help="word to show its count")
    parser.add_argument("filename", help="file to read from")
    args = parser.parse_args()
    word = args.word
    filename = ('../' + args.filename)
    if filename[-4:] != '.csv':
        ERR('Error: {} does not exist!\n\n'.format(args.filename))
    else:
        Wdict = read_words(filename)
        Wcount(Wdict, word)

if __name__ == '__main__':
    main()