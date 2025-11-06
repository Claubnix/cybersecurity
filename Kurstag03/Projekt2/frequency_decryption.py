import frequency_decryption_encrypted_texts


# port a list into a dictionary
def dictify(some_list):
    return {x[0]: x[1] for x in some_list}


# get value from an item, for example the value of an element in a dictionary
def get_value(item):
    return item[1]


# return a dictionary with each character in a text and its frequency within said text in percent
def get_frequencies(text):
    all_freq = {}

    for c in text:
        if c.isalpha():
            if c in all_freq:
                all_freq[c] += 1
            else:
                all_freq[c] = 1

    total = sum(all_freq.values())

    for key, value in all_freq.items():
        all_freq[key] = value / total * 100

    return dictify(sorted(all_freq.items(), key=get_value, reverse=True))


def decrypt_text(text, encryption_key):
    for k, v in encryption_key.items():
        text = text.replace(k, v)

    return text


text1 = frequency_decryption_encrypted_texts.encrypted_text_1
encryption_key_1 = {}
encryption_key_1.update({'a': 'E'})
encryption_key_1.update({'b': 'F'})
encryption_key_1.update({'c': 'Ä'})
encryption_key_1.update({'d': 'B'})
encryption_key_1.update({'e': 'J'})
encryption_key_1.update({'f': 'R'})
encryption_key_1.update({'g': 'T'})
encryption_key_1.update({'h': 'C'})
encryption_key_1.update({'i': 'Z'})
encryption_key_1.update({'j': 'G'})
encryption_key_1.update({'k': 'I'})
encryption_key_1.update({'l': 'W'})
encryption_key_1.update({'m': 'M'})
encryption_key_1.update({'n': ''})
encryption_key_1.update({'o': 'S'})
encryption_key_1.update({'p': 'N'})
encryption_key_1.update({'q': 'D'})
encryption_key_1.update({'r': 'H'})
encryption_key_1.update({'s': 'A'})
encryption_key_1.update({'t': 'X'})
encryption_key_1.update({'u': 'V'})
encryption_key_1.update({'v': 'O'})
encryption_key_1.update({'w': 'Ö'})
encryption_key_1.update({'x': 'K'})
encryption_key_1.update({'y': 'L'})
encryption_key_1.update({'z': 'Ü'})
encryption_key_1.update({'ä': 'P'})
encryption_key_1.update({'ö': 'U'})
encryption_key_1.update({'ü': ''})

text2 = frequency_decryption_encrypted_texts.encrypted_text_2
encryption_key_2 = {}
encryption_key_2.update({'a': 'a'})
encryption_key_2.update({'b': 'b'})
encryption_key_2.update({'c': 'c'})
encryption_key_2.update({'d': 'd'})
encryption_key_2.update({'e': 'e'})
encryption_key_2.update({'f': 'f'})
encryption_key_2.update({'g': 'g'})
encryption_key_2.update({'h': 'h'})
encryption_key_2.update({'i': 'i'})
encryption_key_2.update({'j': 'j'})
encryption_key_2.update({'k': 's'})
encryption_key_2.update({'l': 'l'})
encryption_key_2.update({'m': 'm'})
encryption_key_2.update({'n': 'n'})
encryption_key_2.update({'o': 'o'})
encryption_key_2.update({'p': 'p'})
encryption_key_2.update({'q': 'q'})
encryption_key_2.update({'r': 'r'})
encryption_key_2.update({'s': 's'})
encryption_key_2.update({'t': 't'})
encryption_key_2.update({'u': 'D'})
encryption_key_2.update({'v': 'E'})
encryption_key_2.update({'w': 'w'})
encryption_key_2.update({'x': 'x'})
encryption_key_2.update({'y': 'y'})
encryption_key_2.update({'z': 'z'})
encryption_key_2.update({'ä': 'ä'})
encryption_key_2.update({'ö': 'ö'})
encryption_key_2.update({'ü': 'ü'})

text3 = frequency_decryption_encrypted_texts.encrypted_text_3
encryption_key_3 = {}
encryption_key_3.update({'a': 'a'})
encryption_key_3.update({'b': 'b'})
encryption_key_3.update({'c': 'c'})
encryption_key_3.update({'d': 'd'})
encryption_key_3.update({'e': 'e'})
encryption_key_3.update({'f': 'f'})
encryption_key_3.update({'g': 'g'})
encryption_key_3.update({'h': 'h'})
encryption_key_3.update({'i': 'i'})
encryption_key_3.update({'j': 'j'})
encryption_key_3.update({'k': 'k'})
encryption_key_3.update({'l': 'l'})
encryption_key_3.update({'m': 'm'})
encryption_key_3.update({'n': 'n'})
encryption_key_3.update({'o': 'o'})
encryption_key_3.update({'p': 'p'})
encryption_key_3.update({'q': 'q'})
encryption_key_3.update({'r': 'r'})
encryption_key_3.update({'s': 's'})
encryption_key_3.update({'t': 't'})
encryption_key_3.update({'u': 'u'})
encryption_key_3.update({'v': 'v'})
encryption_key_3.update({'w': 'w'})
encryption_key_3.update({'x': 'x'})
encryption_key_3.update({'y': 'y'})
encryption_key_3.update({'z': 'z'})
encryption_key_3.update({'ä': 'ä'})
encryption_key_3.update({'ö': 'ö'})
encryption_key_3.update({'ü': 'ü'})

text4 = frequency_decryption_encrypted_texts.encrypted_text_4
encryption_key_4 = {}
encryption_key_4.update({'a': 'a'})
encryption_key_4.update({'b': 'b'})
encryption_key_4.update({'c': 'c'})
encryption_key_4.update({'d': 'd'})
encryption_key_4.update({'e': 'e'})
encryption_key_4.update({'f': 'f'})
encryption_key_4.update({'g': 'g'})
encryption_key_4.update({'h': 'h'})
encryption_key_4.update({'i': 'i'})
encryption_key_4.update({'j': 'j'})
encryption_key_4.update({'k': 'k'})
encryption_key_4.update({'l': 'l'})
encryption_key_4.update({'m': 'm'})
encryption_key_4.update({'n': 'n'})
encryption_key_4.update({'o': 'o'})
encryption_key_4.update({'p': 'p'})
encryption_key_4.update({'q': 'q'})
encryption_key_4.update({'r': 'r'})
encryption_key_4.update({'s': 's'})
encryption_key_4.update({'t': 't'})
encryption_key_4.update({'u': 'u'})
encryption_key_4.update({'v': 'v'})
encryption_key_4.update({'w': 'w'})
encryption_key_4.update({'x': 'x'})
encryption_key_4.update({'y': 'y'})
encryption_key_4.update({'z': 'z'})
encryption_key_4.update({'ä': 'ä'})
encryption_key_4.update({'ö': 'ö'})
encryption_key_4.update({'ü': 'ü'})

# uncomment to try to encrypt first text
#print(decrypt_text(text1, encryption_key_1))
#print(get_frequencies(text1))

# uncomment to try to encrypt second text
print(decrypt_text(text2, encryption_key_2))
print(get_frequencies(text2))

# uncomment to try to encrypt third text
#print(decrypt_text(text3, encryption_key_3))
#print(get_frequencies(text3))

# uncomment to try to encrypt fourth text
#print(decrypt_text(text4, encryption_key_4))
#print(get_frequencies(text4))

# uncomment to try to encrypt third and fourth text together
#text34 = text3+"\n--------------------------------\n"+text4
#print(decrypt_text(text34, encryption_key_3))
#print(get_frequencies(text34))
