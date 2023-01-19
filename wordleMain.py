import os

#allWords = list()

def newGame():
    #global allWords
    #base_path = "Desktop"
    #filename = "5letterwords.txt"
    #path_to_file = os.path.join(base_path, filename)
    #with open(path_to_file,'r') as file:
    allWords = list()
    with open("5letterwords.txt",'r') as file:
        for line in file:
            for word in line.split():
                allWords.append(word)
    return allWords


def NotInWord(letters, words):
    possible = list()
    for word in words:
        good = True
        for letter in letters:
            if (letter in word):
                good = False
        if (good):
            possible.append(word)
    return possible


def InWord(letter, position, words):
    possible = list()
    good = False
    for word in words:
        good = False
        for i in range(len(word)):
            if (word[i] == letter):
                if (i != position):
                    good = True
        if (good):
            if (word[position] != letter):
                possible.append(word)
    return possible


def CorrectLetter(letter, position, words):
    possible = list()
    for word in words:
        if (word[position] == letter):
            possible.append(word)
    return possible
