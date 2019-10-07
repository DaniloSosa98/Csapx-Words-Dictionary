import csv
import argparse
import sys
from collections import Counter
import string
import matplotlib.pyplot as plt
import numpy as np

ERR = sys.stderr.write
d = dict.fromkeys(string.ascii_lowercase, 0)

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

def total_count(Dtotal: dict) -> dict:
    for word in Dtotal:
        count = 0
        for element in Dtotal[word].get('occur'):
            count += int(element)
        tempLet = Counter(word)
        for letter in tempLet:
            tempLet[letter] = tempLet.get(letter) * count

        Dtotal[word] = {'total': count, 'letters': tempLet}


    return Dtotal

def letter_count(Dtotal: dict, keyL: list, valueL: list) -> None:
    total = 0
    for word in Dtotal:
        for letter in Dtotal[word].get('letters'):
            Ltotal =  Dtotal[word].get('letters').get(letter)

            d[letter] = d.get(letter) + Ltotal
            total += Ltotal

    for letter in d:
        d[letter] = d.get(letter)/total

    for letter in d:
        keyL.append(letter)
        valueL.append(d[letter])

def main() -> None:

    global keyL, valueL
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--output", action="store_true", help="display letter frequencies to standard output")
    parser.add_argument("-p","--plot", action="store_true", help="plot letter frequencies using matplotlib")
    parser.add_argument("filename", help="a comma separated value unigram file")
    args = parser.parse_args()
    filename = ('../' + args.filename)

    if filename[-4:] != '.csv':
        ERR('Error: {} does not exist!\n\n'.format(args.filename))
    else:
        keyL = []
        valueL = []
        Wdict = read_words(filename)
        Wdict = total_count(Wdict)
        letter_count(Wdict, keyL, valueL)

    if args.output:
        for key in d:
            print(key, ':', d[key])
    if args.plot:
        xpos = np.arange(len(keyL))
        plt.bar(xpos, valueL)
        plt.xticks(xpos, keyL)
        plt.ylabel("Frequency")
        plt.xlabel("Letter")
        plt.title('Letter Frequencies: {}'.format(args.filename))
        plt.show()


if __name__ == '__main__':
    main()