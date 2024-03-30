# File: writer-bot-ht.py
# Author: Sam Abbott
# Purpose: Generate pseudo-random text from a file and print

import random

SEED = 8
NONWORD = "@"

def main():
    sfile_name = input()
    sfile = open(sfile_name, "r")

    try:
        M = int(input())    # M = size of hash table
    except TypeError:
        exit(1)
    try:
        n = int(input())    # n = desired length of prefix
    except TypeError:
        exit(1)

    if n < 1:
        print("ERROR: specified prefix size is less than one")
        exit(1)

    try:
        text_size = int(input()) 
    except TypeError:
        exit(1)
    
    if text_size < 1:
        print("ERROR: specified size of the generated text is less than one")
        exit(1)

    random.seed(SEED)
    table = build_markov_table(sfile, n, M)
    sfile.seek(0)
    text_ls = generate_random_text(table, text_size, sfile, n)
    print_text(text_ls)

class Hashtable:
    """
    Each prefix (string) is hashed based on the length and stored at the hash index 
    in a list containing the prefix in the first entry and a list of suffixes (strings)   
    in the second entry of the list
    """
    def __init__(self, size):
        self._size = size
        self._pairs = [NONWORD] * size # Pairs is the list of prefixes and suffix lists

    def put(self, key, value):
        """
        Uses the hash function to determine the index at which the prefix/suffix pair is 
        stored, then adds the pair if the entry is NONWORD. If not, iterates down _pairs
        until it finds NONWORD, or up _pairs if the beginning of pairs is reached
        Params: prefix, suffix list
        """
        if self._pairs[self._hash(key)][0] == NONWORD or self._pairs[self._hash(key)][0] == key:
            self._pairs[self._hash(key)] = [key, value]
        else:
            hash_index = self._hash(key) - 1
            while self._pairs[hash_index][0] != NONWORD:
                hash_index -= 1
                if hash_index == 0:     # Beginning of _pairs reached
                    break
                    hash_index = self._hash(key) + 1    # Resetting index
                    while self._pairs[hash_index][0] != NONWORD:
                        hash_index += 1
                        break
            self._pairs[hash_index] = [key, value]

    def get(self, key):
        """
        Determines if the given prefix is in pairs and returns if so
        Parans: prefix
        Returns: Suffix list if found, None if not
        """
        for i in range(len(self._pairs)):   # for loop instead of while, no runtime issues
            if self._pairs[i][0] == key:
                return self._pairs[i][1]
        return None

    def __contains__(self, key): 
        """
        Determines if the given prefix is in _pairs
        Params: prefix
        Returns: True if prefix is found, False if not
        """
        for i in range(len(self._pairs)):   # Could've used get() != None, but I want points
            if self._pairs[i][0] == key:
                return True
        return False

    def _hash(self, key):
        p = 0
        for c in key:
            p = 31 * p + ord(c)
        p %= self._size
        return p

def build_markov_table(sfile, prefix_len, M):
    """
    Initializes hash table from given file and prefix length with prefixes
    as strings for keys and a list of suffixes as values for those keys.
    (Note: the initialization uses the Markov Chain Analysis method)
    Params: Text file, prefix length, size of hash table
    Returns: Hash table of prefixes and suffixes
    """

    prefix = ""
    suffix = ""
    markov_table = Hashtable(M)
    
    suffix_ls = []
    sfile_text = sfile.read().split()
    nonword_ls = [NONWORD] * prefix_len

    for i in range(len(nonword_ls)):    # Using NONWORD as prefixes to first suffixes in text
        if i == 1:
            nonword_ls[-i] = sfile_text[i - 1]
        elif i > 1:
            nonword_ls[-i] = nonword_ls[-i + 1]
            nonword_ls[-i + 1] = sfile_text[i - 1]

        nonword_str = ' '.join(nonword_ls)
        markov_table.put(nonword_str, [sfile_text[i]])

    i = 0

    while (i + prefix_len) < len(sfile_text): 
        suffix_ls = []
        prefix = ' '.join(sfile_text[i:(i + prefix_len)])
        suffix = sfile_text[(i + prefix_len)]
        suffix_ls.append(suffix)

        if markov_table.__contains__(prefix) == False:
            markov_table.put(prefix, [suffix])
        else:
            m_suffix_ls = markov_table.get(prefix)
            m_suffix_ls.append(suffix)

        i += 1
    return markov_table

def generate_random_text(markov_table, num_words, sfile, prefix_len):
    """
    Chooses random suffix corresponding to each prefix, setting the next prefix
    to include the chosen suffix as the last word and continuing until the desired
    number of words is generated
    Params: Hash table of prefixes and suffixes, number of words to be generated, text file,
    and the length of the prefix
    Returns: List of random text
    """

    random_text = []
    sfile_t = sfile.read().split()
    i, j, iteration = 0, 0, 1
        
    if iteration < 2:     # Initializing first prefix from the text file list
        prefix = []
        for i in range(prefix_len):
            prefix.append(sfile_t[i])
            random_text.append(sfile_t[i])
        prefix = ' '.join(prefix)
        iteration += 1

    while markov_table.get(prefix) != None:
        suffix = markov_table.get(prefix)
        if len(suffix) > 1:
            r = random.randint(0, len(suffix) - 1)
            random_text.append(suffix[r])
        else:
            random_text.append(suffix[0])
        prefix = []
        for j in range(prefix_len, 0, -1):    # Set last n words of the random text as next prefix
            prefix.append(random_text[-j])

        prefix = ' '.join(prefix)
        if len(random_text) >= num_words:
            break

    return random_text


def print_text(text_ls):
    """
    Prints random text list, 10 words per line (can be less than 10 on last line)
    Params: List of random words to print
    Returns: None
    """

    i, j = 1, 1
    while i <= ((len(text_ls) // 10 + 1)):      # Determines number of lines
        while j < i * 10:      # j coninues until it reaches the end of the text file
            if j == 1 and i == 1:
                print(text_ls[0] + ' ', end='')
            try:        
                if j < i * 10 - 1:      # Determines if a space is needed at the end of the word
                    if not j == len(text_ls) - 1:      
                        print(text_ls[j] + ' ', end='')
                    else:       # Only occurs when the text does not reach the end of the line
                        print(text_ls[j], end='')       
                        print()
                        break
                else:
                    print(text_ls[j], end='')
            except IndexError:      # Needed only when number of words not a multiple of 10
                break
            j += 1
        i += 1
        if i <= len(text_ls) // 10 + 1:
            print()
    
main()