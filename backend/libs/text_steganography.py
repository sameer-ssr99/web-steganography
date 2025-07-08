import os

def encode_text(file_path, message):
    dir_path = os.path.dirname(file_path)
    processed_path = os.path.join(dir_path, 'processed')
    os.makedirs(processed_path, exist_ok=True)

    encoded_file = os.path.join(processed_path, 'stego_' + os.path.basename(file_path))

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().split()

    if len(message) > len(content) * 2:
        raise ValueError("Message too long to hide in the given file.")

    def EncodeTheText(text):
        i = 0
        add = ''
        while i < len(text):
            t = ord(text[i])
            if 32 <= t <= 64:
                t1 = t + 48
                t2 = t1 ^ 170
                res = bin(t2)[2:].zfill(8)
                add += "0011" + res
            else:
                t1 = t - 48
                t2 = t1 ^ 170
                res = bin(t2)[2:].zfill(8)
                add += "0110" + res
            i += 1
        return add + "111111111111"

    binary = EncodeTheText(message)
    ZWC = {"00": u'\u200C', "01": u'\u202C', "11": u'\u202D', "10": u'\u200E'}
    ii = 0

    with open(encoded_file, 'w', encoding='utf-8') as out:
        while ii < len(binary):
            s = content[int(ii / 12)]
            w = ""
            for j in range(0, 12, 2):
                zwc_pair = binary[ii + j: ii + j + 2]
                w += ZWC[zwc_pair]
            s1 = s + w
            out.write(s1 + " ")
            ii += 12

        t = int(len(binary) / 12)
        while t < len(content):
            out.write(content[t] + " ")
            t += 1

    return encoded_file


def decode_text(file_path):
    def BinaryToDecimal(binary):
        return int(binary, 2)

    ZWC_reverse = {
        u"\u200C": "00",
        u'\u202C': "01",
        u'\u202D': "11",
        u'\u200E': "10"
    }

    temp = ''
    with open(file_path, 'r', encoding="utf-8") as file4:
        for line in file4:
            for word in line.split():
                binary_extract = ""
                for letter in word:
                    if letter in ZWC_reverse:
                        binary_extract += ZWC_reverse[letter]
                if "111111111111" in binary_extract:
                    binary_extract = binary_extract.split("111111111111")[0]
                temp += binary_extract

    i = 0
    a = 0
    b = 4
    c = 4
    d = 12
    final = ''
    while i < len(temp):
        t3 = temp[a:b]
        a += 12
        b += 12
        i += 12
        t4 = temp[c:d]
        c += 12
        d += 12
        if t3 == "0110":
            for j in range(0, len(t4), 8):
                decimal_data = BinaryToDecimal(t4[j:j + 8])
                final += chr((decimal_data ^ 170) + 48)
        elif t3 == "0011":
            for j in range(0, len(t4), 8):
                decimal_data = BinaryToDecimal(t4[j:j + 8])
                final += chr((decimal_data ^ 170) - 48)

    return final
