"""This is my Huffman coding module"""

from bitstring import BitArray
import time
start_time = time.time()

# Note : all code used for converting binary string to .bin file is code provided by Dr. Camargo


class Node:
    def __init__(self, freq, char, left=None, right=None):
        self.freq = freq
        self.left = left
        self.right = right
        self.char = char
        self.bin = ''

    def printTree(self, dict1, prevBinRepr=""):
        binRepr = prevBinRepr + str(self.bin)
        if self.left:
            self.left.printTree(dict1, binRepr)
        if self.right:
            self.right.printTree(dict1, binRepr)
        if not self.right and not self.left:
            # We add our binary representation to a dict
            dict1[self.char] = binRepr
            # print(self.char, end=" :")
            # print(binRepr)


def frequency(text):
    dictionary = {}
    # Make a dictionary with key character and value frequency
    for keys in text:
        dictionary[keys] = dictionary.get(keys, 0) + 1
    # Sort dictionary by frequency
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1]))
    return sorted_dict


def decode(firstNode, ctr, bintxt, decoded):
    if firstNode is None:
        return ctr
    # When a end-node is found, return string with added char and index
    if firstNode.left is None and firstNode.right is None:
        # print(firstNode.char, end="")
        decoded.append(firstNode.char)
        return ctr, decoded
    # if we havent reached a end-node, increment index and go left/right depending on encoded string
    ctr = ctr + 1
    firstNode = firstNode.left if bintxt[ctr] == "0" else firstNode.right
    return decode(firstNode, ctr, bintxt, decoded)


def print_decoded(encoded_string, Tree):
    index = -1
    decoded_str = []
    while index < len(encoded_string) - 6:
        char = decode(Tree, index, encoded_string, decoded_str)
        index = char[0]
    return decoded_str


def HuffmanTree(sorted_list):
    # first, make a list of nodes from the sorted dictionary of frequencies
    nodes = []
    for i in sorted_list:
        nodes.append(Node(sorted_list[i], i))
    # While there are still nodes to insert
    while len(nodes) > 1:
        nodes[0].bin = 0  # Attribute 0 to left node
        nodes[1].bin = 1  # Attribute 1 to right node

        # Combine 2 lowest frequency nodes to make a new node
        z = Node(freq=nodes[0].freq + nodes[1].freq, char=nodes[0].char + nodes[1].char, left=nodes[0], right=nodes[1])

        # Remove individual lowest freq nodes
        nodes.remove(nodes[0])
        nodes.remove(nodes[0])

        # Add the new node to our list
        nodes.append(z)

        # Sort our list by ascending frequency
        nodes = sorted(nodes, key=lambda j: j.freq)
    return nodes[0]


def decompress(binfile, decodedtxt, tree, encoding=""):
    if encoding != "":
        with open(binfile, 'rb') as f:
            b = BitArray(f.read())
        with open(decodedtxt, "w", encoding=encoding) as outfile:
            new_str = print_decoded(b.bin, tree)
            new_str = "".join(new_str)
            outfile.write(new_str)
    else:
        with open(binfile, 'rb') as f:
            b = BitArray(f.read())
        with open(decodedtxt, "w") as outfile:
            new_str = print_decoded(b.bin, tree)
            new_str = "".join(new_str)
            outfile.write(new_str)


def Huffman_Coding(text, enc_name, encoding=""):
    binStr = ""
    if encoding != "":
        with open(text, "r", encoding=encoding) as infile, open(enc_name, "wb") as outfile:
            newText = infile.read()
            newText = newText.rstrip()

            freq = frequency(newText)
            tree = HuffmanTree(freq)
            Codes = {}
            tree.printTree(Codes)
            l = []
            for char in newText:
                l.append(Codes[char])
            binStr = binStr.join(l)
            a = BitArray(bin=binStr)
            a.tofile(outfile)
    else:
        with open(text, "r") as infile, open(enc_name, "wb") as outfile:
            newText = infile.read()
            newText = newText.rstrip()

            freq = frequency(newText)
            tree = HuffmanTree(freq)
            Codes = {}
            tree.printTree(Codes)
            l = []
            for char in newText:
                l.append(Codes[char])
            binStr = binStr.join(l)
            a = BitArray(bin=binStr)
            a.tofile(outfile)
    return tree, freq, Codes


# Normal compression and decompression of MOT in English, French and Portuguese
MOT_Eng = Huffman_Coding("Moon-Of-Treason.txt", "M-O-T-Encoded.bin")
decompress("M-O-T-Encoded.bin", "M-O-T-DecodeEng.txt", MOT_Eng[0])
MOT_Fr = Huffman_Coding("M-O-T-French.txt", "M-O-T-FrEncoded.bin")
decompress("M-O-T-FrEncoded.bin", "M-O-T-FrDecoded.txt", MOT_Fr[0])
MOT_Por = Huffman_Coding("M-O-T-Portuguese.txt", "M-O-T-PrEncoded.bin", encoding="utf8")
decompress("M-O-T-PrEncoded.bin", "M-O-T-PrDecoded.txt", MOT_Por[0], encoding="utf8")


# Coding Portuguese text using English encoding
with open("M-O-T-Portuguese.txt", "r", encoding="utf8") as infile, open("M-O-T-Eng2Pr.bin", "wb") as outfile:
    binStr = ""
    newText = infile.read()
    newText = newText.rstrip()

    freq = MOT_Eng[1]
    Codes = {}
    # I add new characters that are missing from my tree, and create a new tree
    for char in newText:
        if char not in Codes:
            freq[char] = 1
    tree = HuffmanTree(freq)
    tree.printTree(Codes)
    l = []
    for char in newText:
        l.append(Codes[char])
    new_str1 = print_decoded(binStr, tree)
    binStr = binStr.join(l)
    a = BitArray(bin=binStr)
    a.tofile(outfile)
    decompress("M-O-T-Eng2Pr.bin", "M-O-T-Eng2Pr.txt", tree, encoding="utf8")

# Coding French text using English encoding
with open("M-O-T-French.txt", "r", encoding="utf8") as infile, open("M-O-T-Eng2Fr.bin", "wb") as outfile:
    binStr = ""
    newText = infile.read()
    newText = newText.rstrip()

    freq = MOT_Eng[1]
    Codes = {}
    # I add new characters that are missing from my tree, and create a new tree
    for char in newText:
        if char not in Codes:
            freq[char] = 1
    tree = HuffmanTree(freq)
    tree.printTree(Codes)
    l = []
    for char in newText:
        l.append(Codes[char])
    new_str1 = print_decoded(binStr, tree)
    binStr = binStr.join(l)
    a = BitArray(bin=binStr)
    a.tofile(outfile)
    decompress("M-O-T-Eng2Fr.bin", "M-O-T-Eng2Fr.txt", tree, encoding="utf8")

#
# Normal compression and decompression of MOT in English, French and Portuguese
ST_Eng = Huffman_Coding("SomeTrees.txt", "ST-Encoded.bin", encoding="utf8")
decompress("ST-Encoded.bin", "STDecodeEng.txt", ST_Eng[0], encoding="utf8")
ST_Fr = Huffman_Coding("ST-French.txt", "STFrEncoded.bin", encoding="utf8")
decompress("STFrEncoded.bin", "STFrDecoded.txt", ST_Fr[0], encoding="utf8")
ST_Por = Huffman_Coding("ST-Por.txt", "STPrEncoded.bin", encoding="utf8")
decompress("STPrEncoded.bin", "STPrDecoded.txt", ST_Por[0], encoding="utf8")

# Coding English text using Portuguese encoding
with open("SomeTrees.txt", "r", encoding="utf8") as infile, open("STPr2Eng.bin", "wb") as outfile:
    binStr = ""
    newText = infile.read()
    newText = newText.rstrip()

    freq = ST_Por[1]
    Codes = {}
    # I add new characters that are missing from my tree, and create a new tree
    for char in newText:
        if char not in Codes:
            freq[char] = 1
    tree = HuffmanTree(freq)
    tree.printTree(Codes)
    l = []
    for char in newText:
        l.append(Codes[char])
    new_str1 = print_decoded(binStr, tree)
    binStr = binStr.join(l)
    a = BitArray(bin=binStr)
    a.tofile(outfile)
    decompress("STPr2Eng.bin", "STPr2Eng.txt", tree, encoding="utf8")


# Coding French text using Portuguese encoding
with open("ST-French.txt", "r", encoding="utf8") as infile, open("STPr2Fr.bin", "wb") as outfile:
    binStr = ""
    newText = infile.read()
    newText = newText.rstrip()

    freq = ST_Por[1]
    Codes = {}
    # I add new characters that are missing from my tree, and create a new tree
    for char in newText:
        if char not in Codes:
            freq[char] = 1
    tree = HuffmanTree(freq)
    tree.printTree(Codes)
    l = []
    for char in newText:
        l.append(Codes[char])
    new_str1 = print_decoded(binStr, tree)
    binStr = binStr.join(l)
    a = BitArray(bin=binStr)
    a.tofile(outfile)
    #decompress("STPr2Fr.bin", "STPr2Fr.txt", tree, encoding="utf8")

fib = Huffman_Coding("fib41.txt", "fibEncoded.bin")
print("compressed")
decompress("fibEncoded.bin", "fibDecoded.txt", fib[0])
print("finished")

einstein = Huffman_Coding("einstein.de.txt", "einsteinEnc.bin")
print("compressed")
decompress("einsteinEnc.bin", "einsteinDec.txt", einstein[0])
print("finished")

dblp = Huffman_Coding("dblp.xml.00001.1", "dblpEnc.bin")
print("compressed")
decompress("dblpEnc.bin", "dblDec.txt", dblp[0])

print("--- %s seconds ---" % (time.time() - start_time))