# File: rhymes.py
# Author: Sam Abbott
# Purpose: Find perfect rhymes of a given word in a file
# CSc 120, Spring 2019, Dr. O'Bagly

def main():
    pron_fname = input()
    try:
        pron_file = open(pron_fname, "r")
    except FileNotFoundError:
        print("ERROR: Could not open file " + pron_fname)
        exit(1)
    wm = WordMap()
    pron_dict = wm.build_pron_dict(pron_file)
    inp_word = input()
    wm.find_rhymes(inp_word, pron_dict)

class Word:
    def __init__(self, curr_word, pron_dict):
        self._curr_word = curr_word
        self._pron_dict = pron_dict

    def value(self):
        return self._curr_word

    def __str__(self):
        print(str(self._curr_word))
    
    def get_stressed_index(self):
        # Determines the index of the primary stress phoneme in the current word instance

        self._pron_ls = Word(self._curr_word, self._pron_dict).get_prons(self._pron_dict)
        self._found = -1

        for pron in self._pron_ls:
            for i in range(len(pron)):
                if len(pron[i]) == 3:
                    if pron[i][2] == '1':
                        self._found = i
                        break

        return self._found
    
    def get_prons(self, pron_dict):
        # Gets pronunciations of the current word from the pronunciation dictionary

        try:    # Try/except statement is used here to  determine if the given word is in the pron. dict.
            prons = pron_dict[Word(self._curr_word, pron_dict).value()]
        except KeyError:
            print("ERROR: the word input by the user is not in the pronunciation dictionary " + str(self._curr_word))
            exit(1)

        return prons

    def is_rhyme(self, inp_word, inp_pron):
        # Determines if a given word is a perfect rhyme to another, 
        # returns True if a match is found, False if not

        self._inp_stressed = Word(inp_word, self._pron_dict).get_stressed_index()
        self._curr_stressed = Word(self._curr_word, self._pron_dict).get_stressed_index()
        curr_prons = Word(self._curr_word, self._pron_dict).get_prons(self._pron_dict)

        for pron in curr_prons:
            if (inp_pron == pron) or (self._curr_stressed == -1):
                continue
            if pron[self._curr_stressed:] == inp_pron[self._inp_stressed:]:
                if (self._inp_stressed > 0) and (self._curr_stressed > 0):
                    if (pron[self._curr_stressed - 1] != inp_pron[self._inp_stressed - 1]):
                        return True
                elif (self._inp_stressed == 0) and (self._curr_stressed == 0):
                    continue
                else:
                    return True
        return False


class WordMap:
    def __init__(self):
        self._pron_list = []
        self._pron_dict = {}

    def build_pron_dict(self, pron_file):
        # Initializing dictionary from file of pronunciations with keys as words
        # and values as lists of phonemes in lists of in pronunciations 

        for line in pron_file.readlines():
            self._pron_list = line.strip().split()
            self._curr_word = Word(self._pron_list[0].lower(), self._pron_dict).value()
            if self._curr_word not in self._pron_dict:
                self._pron_dict[self._curr_word] = [self._pron_list[1:]]
            else:
                self._pron_dict[self._curr_word].append(self._pron_list[1:])

        return self._pron_dict
    
    def find_rhymes(self, inp_word, pron_dict):
        # Finds all perfect rhymes in a dictionary for a given word by checking if 1) 
        # primary stress phonemes match, 2) subsequent phonemes match and 3) the preceding 
        # phoneme differs.

        inp_prons = Word(inp_word, pron_dict).get_prons(pron_dict)
        rhyme_list = []
        for pron in inp_prons:  # Looping through pronunciations of given word
            for curr_word, prons in self._pron_dict.items():    
                found = Word(curr_word, pron_dict).is_rhyme(inp_word, pron)
                if found and (Word(curr_word, pron_dict).value() not in rhyme_list):
                    rhyme_list.append(Word(curr_word, pron_dict).value())
        for i in range(len(rhyme_list)):
            print(rhyme_list[i])

main()