# File: rhymes.py
# Author: Sam Abbott
# Purpose: Find perfect rhymes of a given word in a file
# CSc 120, Spring 2019, Dr. O'Bagly

def init():
    pron_fname = input()
    pron_file = open(pron_fname, "r")

    return pron_file

def pron_dict_from_file(pron_file):
    # Initializing dictionary from file of pronunciations with keys as words
    # and values as lists of phonemes in lists of in pronunciations 
    # Params: Pronunciation text file
    # Returns:
    pron_list = []
    pron_dict = {}

    for line in pron_file.readlines():
        pron_list = line.strip().split()
        word = pron_list[0].lower()
        if word not in pron_dict:
            pron_dict[word] = [pron_list[1:]]
        else:
            pron_dict[word].append(pron_list[1:])
    return pron_dict

def find_all_rhymes(pron_dict, word):
    # Finds all perfect rhymes in a dictionary for a given word by checking if 1) 
    # primary stress phonemes match, 2) subsequent phonemes match and 3) the preceding 
    # phoneme differs.
    # Params: Dictionary of words and their pronunciations, word to find rhymes for
    # Returns: List of words rhyming with given word

    word_prons = []
    inp_stressed_index = 0
    phoneme_stressed_index = 0
    rhyme_list = []

    word_prons = pron_dict[word.lower()]

    for word in word_prons:     # Looping through pronunciations of given word
        inp_stressed_index = get_stressed_index(word)
        if inp_stressed_index == -1:
            continue
        for key, pron_ls in pron_dict.items():
            for pron in pron_ls:
                phoneme_stressed_index = get_stressed_index(pron)
                if (word == pron) or (phoneme_stressed_index == -1):
                    continue
                if pron[phoneme_stressed_index:] == word[inp_stressed_index:]:
                    if (inp_stressed_index > 0) and (phoneme_stressed_index > 0):
                        if (pron[phoneme_stressed_index - 1] != word[inp_stressed_index - 1]):
                            rhyme_list.append(key)
                    elif (inp_stressed_index == 0) and (phoneme_stressed_index == 0):
                        continue
                    else:
                        rhyme_list.append(key)
    return rhyme_list

def get_stressed_index(phoneme_list):
    # Finds the index of the primary stress phoneme
    # Params: List of phonemes
    # Returns: Index of primary stress phoneme, -1 if not found

    found = -1

    for i in range(len(phoneme_list)):
        if len(phoneme_list[i]) == 3:
            if phoneme_list[i][2] == '1':
                found = i

    return found


def main():
    pron_file = init()
    pron_dict = pron_dict_from_file(pron_file)
    word1, word2, word3 = input(), input(), input()
    rhyme_list = find_all_rhymes(pron_dict, input())
    rhyme_list.sort()
    for word in rhyme_list:
        print(word.upper())

main()