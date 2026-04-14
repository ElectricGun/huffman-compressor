import json

def decode(root, byte_array, padding):
    decoded_text = ""
    current_node = root

    for h, byte in enumerate(byte_array):
        on_last_byte = h == len(byte_array) - 1

        for i in range(8):
            if on_last_byte and i >= (8 - padding):
                break

            bit = (byte >> (7 - i)) & 1

            if bit == 0:
                current_node = current_node["left"]
            else:
                current_node = current_node["right"]
            
            if current_node["left"] is None and current_node["right"] is None:
                decoded_text += current_node["symbol"]
                current_node = root
    
    return decoded_text

print("Stage 1: Reading metadata...")

with open("compressed_output/metadata.json") as f:
    meta = json.load(f)

print("Stage 2: Reading data...")

with open("compressed_output/data.bin", "rb") as f:
    byte_array = bytearray(f.read())

padding = meta["padding"]
root_data = meta["root"]

print("Stage 3: Decoding...")

decoded_text = decode(root_data, byte_array, padding)

with open("decompressed_output/decoded.txt", "w") as f:
    f.write(decoded_text)

print("Finished.")
