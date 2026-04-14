import json

class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

def serialize_node(node):
    if node is None:
        return None

    return {
        "freq": node.freq,
        "symbol": node.symbol,
        "left": serialize_node(node.left),
        "right": serialize_node(node.right)
    }

def print_tree(node, indent=""):
    if node is None:
        return

    print(indent + node.symbol)

    if node.left != None:
        print_tree(node.left, indent + "|")

    if node.right != None:
        print_tree(node.right, indent + "|")

def get_codes(node):
    output = {}
    get_codes_helper(node, output)

    return output

def get_codes_helper(node, codes, path=""):
    if node.left == None and node.right == None:
        codes[node.symbol] = path
    else:
        if node.left:
            get_codes_helper(node.left, codes, path + "0")

        if node.right:
            get_codes_helper(node.right, codes, path + "1")

def encode(codes, text):
    encoded_text = ""

    for char in text:
        encoded_text += codes[char]
    
    return encoded_text

with open("to_encode.txt", "r") as f:
    text = f.read()
bag = {}

print("Stage 1: Creating bag of words...")

for letter in text:
    if letter not in bag:
        bag[letter] = Node(1, letter)
    else:
        bag[letter].freq += 1

print("Stage 2: Building tree...")

while len(bag) > 1:
    keys = list(bag.keys())
    smallest_part = keys[0]
    second_smallest_part = keys[1]

    if bag[second_smallest_part].freq < bag[smallest_part].freq:
        smallest_part, second_smallest_part = second_smallest_part, smallest_part
    for key in keys[2:]:
        if bag[key].freq < bag[smallest_part].freq:
            second_smallest_part = smallest_part
            smallest_part = key

        elif bag[key].freq < bag[second_smallest_part].freq:
            second_smallest_part = key

    left = bag[smallest_part]
    right = bag[second_smallest_part]

    combined_node = Node(
        left.freq + right.freq,
        symbol=None,
        left=left,
        right=right
    )

    combined_key = smallest_part + second_smallest_part

    bag.pop(smallest_part)
    bag.pop(second_smallest_part)

    bag[combined_key] = combined_node

print("Stage 3: Encoding text...")

root = list(bag.values())[0]

codes = get_codes(root)

encoded_text = encode(codes, text)

padding = (8 - len(encoded_text) % 8) % 8
encoded_text += "0" * padding

byte_array = bytearray()

for i in range(0, len(encoded_text), 8):
    byte = encoded_text[i:i+8]
    byte_array.append(int(byte, 2))

print("Stage 4: Writing to file...")

metadata = {
    "padding": padding,
    "root": serialize_node(root)
}

with open("compressed_output/data.bin", "wb") as f:
    f.write(byte_array)

with open("compressed_output/metadata.json", "w") as f:
    json.dump(metadata, f)

print("Finished.")