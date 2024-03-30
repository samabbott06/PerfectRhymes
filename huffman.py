# File: huffman.py
# Author: Sam Abbott
# Purpose: Decode a Huffman-encoded sequence of numbers

class Node: 
    """
    Represents one node in the binary search tree with the attributes
    value and the left and right children of the node
    """
    def __init__(self, value): 
        self._value = value 
        self._left = None
        self._right = None
    
    def get_left(self):
        return self._left

    def get_right(self):
        return self._right

    def get_value(self):
        return self._value

def init_tree(inorder, preorder, inorder_start, inorder_end):
    """
    Initializes the binary tree from the given preorder and inorder sequences
    and the beginning and ending indices of the inorder sequence.
    Creates the root node from preorder, then finds the index of the same 
    element in inorder, then initializes the left and right children using the 
    values in inorder to the left or right of the root node value, respectively.
    
    Params: Inorder and preorder lists, starting and ending indices of inorder
    Returns: Binary tree from given inorder and preorder sequences
    """
    if inorder_end < inorder_start:
        return None
    else:
        curr_node = Node(preorder[init_tree.pre_counter])   # Creating node from preorder
        init_tree.pre_counter += 1  # Incrimenting preorder index with counter attribute
        if (inorder_start != inorder_end) == False:
            return curr_node
        else:
            for i in range(inorder_start, inorder_end + 1): # Find index of value from preorder in inorder
                if inorder[i] != curr_node.get_value(): 
                    continue
                else:
                    inorder_index = i
            curr_node._left = init_tree(inorder, preorder, inorder_start, inorder_index - 1) 
            curr_node._right = init_tree(inorder, preorder, inorder_index + 1, inorder_end) 
    return curr_node
  
def print_postorder(node, length):
    """
    Prints the postorder (LRN) sequence using the binary tree
    Params: Root node of the tree, length of the inorder sequence
    Returns: None, prints postorder sequence
    """
    if node is None:
        return
    else:
        print_postorder(node.get_left(), length)
        print_postorder.rcounter += 1   # Counting number of times function is called
        print_postorder(node.get_right(), length)
        print_postorder.lcounter += 1  
        s = print_postorder.lcounter + print_postorder.rcounter
        if s // 2 < length:     # Uses length of inorder sequence to determine print format
            print(node.get_value() + ' ', end='')
        else:
            print(node.get_value())

def decode(encoded, node, tree, dec_seq):
    """
    Decodes the given huffman-encoded string by iterating through the string, moving 
    to the left or right child of the current node if the current number in the string
    is a 1 or 0, respectively. Adds node value to decoded sequence if the children are
    both None.
    Params: Encoded sequence, root node, binary tree, and an empty string
    Returns: Decoded sequence 
    """
    if (node.get_left() is None) and (node.get_right() is None):
        return decode(encoded, tree, tree, dec_seq + str(node.get_value()))
    if node == None or encoded == '':
        return dec_seq
    else:
        if encoded[0] == '1':
            if node.get_right() == None:
                return decode(encoded[1:], node, tree, dec_seq)
            else:
                return decode(encoded[1:], node.get_right(), tree, dec_seq)
        else:
            if node.get_left() == None:
                return decode(encoded[1:], node, tree, dec_seq)
            else:
                return decode(encoded[1:], node.get_left(), tree, dec_seq)
                
def main():
    filename = input("Input file: ")

    try:
        input_file = open(filename, "r")
    except FileNotFoundError:
        print("ERROR: Could not open file " + filename)
        exit(1)

    
    preorder = input_file.readline().strip().split()
    inorder = input_file.readline().strip().split()
    to_decode = input_file.readline().strip()

    dec_seq = ''
    init_tree.pre_counter = 0
    inorder_start = 0
    inorder_end = len(inorder) - 1
    print_postorder.rcounter = 0
    print_postorder.lcounter = 0
    tree = init_tree(inorder, preorder, inorder_start, inorder_end)
    print_postorder(tree, len(inorder))
    print(decode(to_decode, tree, tree, dec_seq))

main()