WORDLE CHEAT:

Goal:
- Easy Mode: returns list of possible words
- Medium Mode: gives a list of synonyms for the possible words
- Hard Mode: gives hints of what letter or type of letter may be in the word
  (ex: there is a 50% chance that the either or both of the letters 'E' and 'F'
  are in the word)

Functions:
- All levels:
    - NotInWord(letters, words)
        Input: an array of letters that are not in the word
        Output: a list of remaining possible words
    - InWord(letter, position, words)
        Input: a letter that is in the word, and the position that it is not at
        Output: a list of remaining possible words
    - CorrectLetter(letter, position, words)
        Input: a letter that is in the right place in the word
        Output: a list of remaining possible words
- Medium level:
    - WordSynonym(word, synonym)
        Input: a possible word choice
        Output: a synonym for that word
    - AllSynonyms(words, synonyms)
        Input: a list of possible word choices
        Output: a list of synonym for those words
- Hard level:
    - LetterProbs(words, probDict)
        Input: a list of possible word choices
        Output: a dictionary with the probability of each letter appearing in the word


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
        for i in range(len(word)):
            if (word[i] == letter):
                if (i != position):
                    good = True
        if (good):
            possible.append(word)
    return possible


def CorrectLetter(letter, position, words):
    possible = list()
    for word in words:
        if (word[position] == letter):
            possible.append(word)
    return possible
