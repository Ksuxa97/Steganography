import codecs
import os

def direct_replacement_method(bin_word):
    print("1. Direct replacement method")

    with codecs.open('steg_text.txt', 'r', 'utf-8') as file:
        filedata = file.read()

    start_size = len(filedata)
    index = 0
    message_byte_size = 0

    for bit in bin_word:
        if bit == "0":
            pos_c = filedata.find("с", index)
            filedata = filedata[:pos_c] + "c" + filedata[pos_c+1:]
            index = pos_c
            message_byte_size += len("c".encode("utf-8"))
        if bit == "1":
            pos_p = filedata.find("р", index)
            filedata = filedata[:pos_p] + "p" + filedata[pos_p+1:]
            index = pos_p
            message_byte_size += len("p".encode("utf-8"))

    with codecs.open('steg_text1.txt', 'w', 'utf-8') as result_file:
        result_file.write(filedata)

    print("Embedment size (bits): " + str(message_byte_size * 8))
    print("Source file size (bytes): " + str(os.path.getsize('steg_text.txt')))
    print("Result file size (bytes): " + str(os.path.getsize('steg_text1.txt')))

    file.close()
    result_file.close()

    return

def extract_bin_word_direct_replacement_method():
    with codecs.open('steg_text1.txt', 'r', 'utf-8') as file:
        filedata = file.read()

    c_index_list = []
    p_index_list = []

    while True:
        if len(c_index_list) == 0:
            c_index_list.append(filedata.find("c"))
            continue
        if filedata.find("c", c_index_list[-1] + 1) == -1:
            break
        c_index_list.append(filedata.find("c", c_index_list[-1] + 1))

    while True:
        if len(p_index_list) == 0:
            p_index_list.append(filedata.find("p"))
            continue
        if filedata.find("p", p_index_list[-1] + 1) == -1:
            break
        p_index_list.append(filedata.find("p", p_index_list[-1] + 1))

    bin_word = ''
    while True:
        if len(p_index_list) == 0 and len(c_index_list) == 0:
            break

        if len(c_index_list) == 0:
            bin_word += '1'
            p_index_list.pop(0)
            continue

        if len(p_index_list) == 0:
            bin_word += '0'
            c_index_list.pop(0)
            continue

        if p_index_list[0] < c_index_list[0]:
            bin_word += '1'
            p_index_list.pop(0)
        else:
            bin_word += '0'
            c_index_list.pop(0)

    return bin_word


def extra_spaces_method(bin_word):
    print("2. Extra spaces method")

    with codecs.open('steg_text.txt', 'r', 'utf-8') as file:
        filedata = file.read()

    index= 0
    message_byte_size = 0

    for bit in bin_word:
        if bit == "0":
            index = filedata.find("\r\n", index)
            filedata = filedata[:index] + " " + filedata[index:]
            index += 2
            message_byte_size += len(" ".encode("utf-8"))
        if bit == "1":
            index = filedata.find("\r\n", index)
            filedata = filedata[:index] + "  " + filedata[index:]
            index += 3
            message_byte_size += len("  ".encode("utf-8"))

    with codecs.open('steg_text2.txt', 'w', 'utf-8') as result_file:
        result_file.write(filedata)

    print("Embedment size (bits): " + str(message_byte_size * 8))
    print("Source file size (bytes): " + str(os.path.getsize('steg_text.txt')))
    print("Result file size (bytes): " + str(os.path.getsize('steg_text2.txt')))

    file.close()
    result_file.close()

    return


def extract_bin_word_extra_Spaces_method():

    with codecs.open('steg_text2.txt', 'r', 'utf-8') as file:
        filedata = file.read()

    bin_word = ''
    index = 0
    while True:
        index = filedata.find("\r\n", index)
        if filedata.find(" ", index-1, index) == -1 and filedata.find("  ", index-2, index) == -1:
            break

        if filedata.find("  ", index - 2, index) != -1:
            bin_word += '1'
            index += 2
            continue

        if filedata.find(" ", index - 1, index+1) != -1:
            bin_word += '0'
            index += 2
            continue
    return bin_word

def service_symbols_method(bin_word):
    print("3. Service symbols method")
    with codecs.open('steg_text.txt', 'r', 'utf-8') as file:
        filedata = file.read()

    index= 0
    message_byte_size = 0

    for bit in bin_word:
        if bit == "0":
            index = filedata.find("\r\n", index) + len("\r\n")
            filedata = filedata[:index] + "\t" + filedata[index:]
            index += 1
            message_byte_size += len("\t".encode("utf-8"))

        if bit == "1":
            index = filedata.find("\r\n", index) + len("\r\n")
            filedata = filedata[:index] + "\t\t" + filedata[index:]
            index += 2
            message_byte_size += len("\t\t".encode("utf-8"))

    with codecs.open('steg_text3.txt', 'w', 'utf-8') as result_file:
        result_file.write(filedata)

    print("Embedment size (bits): " + str(message_byte_size * 8))
    print("Source file size (bytes): " + str(os.path.getsize('steg_text.txt')))
    print("Result file size (bytes): " + str(os.path.getsize('steg_text3.txt')))

    file.close()
    result_file.close()

    return


def extract_bin_word_service_symbols_method():
    with codecs.open('steg_text3.txt', 'r', 'utf-8') as file:
        filedata = file.read()

    bin_word = ''
    index = 0
    index = 0
    while True:
        if filedata.find("\t", index) == -1 and filedata.find("\t\t", index) == -1:
            break
        index = filedata.find("\t", index)
        if filedata.find("\t\t", index, index+2) != -1:
            bin_word += '1'
            index += 2

        if filedata.find("\t", index, index + 1) != -1:
            bin_word += '0'
            index += 1

    return bin_word

def get_word_by_binary(binary):
    word = ""
    while len(binary) != 0:
        bin_letter_1 = int(binary[0:8], 2)
        bin_letter_2 = int(binary[8:16], 2)
        letter = bytearray([bin_letter_1, bin_letter_2]).decode("utf-8")
        word += letter
        binary = binary.replace(binary[0:8]+binary[8:16], "")
    return


def get_binary_word(word: str):

    bin_word = ''

    for letter in word:
        letter_bytearray = bytearray(letter.encode("utf-8"))
        bin_letter = bin(letter_bytearray[0])
        bin_word += bin_letter.replace("0b", "")
        bin_letter = bin(letter_bytearray[1])
        bin_word += bin_letter.replace("0b", "")

    return bin_word

def embed_volume_direct_replacement():

    with codecs.open('steg_text.txt', 'r', 'utf-8') as file:
        filedata = file.read()

    count = 0
    index = 0
    while True:
        index = filedata.find("с", index)
        if index == -1:
            break
        count += 1
        index += 1

    index = 0
    while True:
        index = filedata.find("р", index)
        if index == -1:
            break
        count += 1
        index += 1

    return

def embed_volume_extra_spaces():

    with codecs.open('steg_text.txt', 'r', 'utf-8') as file:
        filedata = file.read()

    count = 0
    index = 0
    while True:
        index = filedata.find("\r\n", index)
        if index == -1:
            break
        count += 1
        index += 1

    return


def main():

    embedded_word = "стеганография"
    print("Emdedded word: " + embedded_word)

    bin_word = get_binary_word(word=embedded_word)
    print("Binary word: "+ bin_word)

    get_word_by_binary(bin_word)

    direct_replacement_method(bin_word)
    extra_spaces_method(bin_word)
    service_symbols_method(bin_word)

    # embed_volume_direct_replacement()
    # embed_volume_extra_spaces()

    return


if __name__ == '__main__':
    main()
