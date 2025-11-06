import random
import frequency_decryption


def encrypt_text(text):
    small_letters = list(map(chr, range(ord('a'), ord('z') + 1)))
    small_letters.append("ä")
    small_letters.append("ö")
    small_letters.append("ü")

    for k, v in frequency_decryption.get_frequencies(text).items():
        c = random.choice(small_letters)
        small_letters.remove(c)
        text = text.replace(k, c)

    return text


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

encryption_key_2 = {}
encryption_key_2.update({'a': 'M'})
encryption_key_2.update({'b': 'W'})
encryption_key_2.update({'c': 'C'})
encryption_key_2.update({'d': 'K'})
encryption_key_2.update({'e': 'Q'})
encryption_key_2.update({'f': 'P'})
encryption_key_2.update({'g': 'Ä'})
encryption_key_2.update({'h': 'U'})
encryption_key_2.update({'i': 'L'})
encryption_key_2.update({'j': 'T'})
encryption_key_2.update({'k': 'Z'})
encryption_key_2.update({'l': 'l'})
encryption_key_2.update({'m': 'I'})
encryption_key_2.update({'n': 'N'})
encryption_key_2.update({'o': 'Ü'})
encryption_key_2.update({'p': 'F'})
encryption_key_2.update({'q': 'J'})
encryption_key_2.update({'r': 'A'})
encryption_key_2.update({'s': 'H'})
encryption_key_2.update({'t': 'G'})
encryption_key_2.update({'u': 'D'})
encryption_key_2.update({'v': 'E'})
encryption_key_2.update({'w': ''})
encryption_key_2.update({'x': 'S'})
encryption_key_2.update({'y': 'Ö'})
encryption_key_2.update({'z': 'O'})
encryption_key_2.update({'ä': 'B'})
encryption_key_2.update({'ö': 'R'})
encryption_key_2.update({'ü': 'V'})

encryption_key_3 = {}
encryption_key_3.update({'a': 'L'})
encryption_key_3.update({'b': 'K'})
encryption_key_3.update({'c': 'N'})
encryption_key_3.update({'d': 'D'})
encryption_key_3.update({'e': 'R'})
encryption_key_3.update({'f': 'F'})
encryption_key_3.update({'g': 'J'})
encryption_key_3.update({'h': 'M'})
encryption_key_3.update({'i': 'E'})
encryption_key_3.update({'j': 'V'})
encryption_key_3.update({'k': 'T'})
encryption_key_3.update({'l': 'Ä'})
encryption_key_3.update({'m': 'O'})
encryption_key_3.update({'n': 'Ö'})
encryption_key_3.update({'o': 'H'})
encryption_key_3.update({'p': 'p'})
encryption_key_3.update({'q': 'Ü'})
encryption_key_3.update({'r': 'A'})
encryption_key_3.update({'s': 'Z'})
encryption_key_3.update({'t': 'C'})
encryption_key_3.update({'u': ''})
encryption_key_3.update({'v': 'P'})
encryption_key_3.update({'w': 'B'})
encryption_key_3.update({'x': 'U'})
encryption_key_3.update({'y': 'S'})
encryption_key_3.update({'z': 'W'})
encryption_key_3.update({'ä': 'Y'})
encryption_key_3.update({'ö': 'I'})
encryption_key_3.update({'ü': 'G'})


encryption_key_4 = encryption_key_3

# uncomment to encrypt first text
#print(frequency_decryption.decrypt_text(frequency_decryption.text1, encryption_key_1))

# uncomment to encrypt second text
#print(frequency_decryption.decrypt_text(frequency_decryption.text2, encryption_key_2))

# uncomment to encrypt third text
#print(frequency_decryption.decrypt_text(frequency_decryption.text3, encryption_key_3))

# uncomment to encrypt fourth text
#print(frequency_decryption.decrypt_text(frequency_decryption.text4, encryption_key_4))
