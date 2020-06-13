from PIL import Image
from math import log10, sqrt
import cv2
import numpy as np
from termcolor import colored

RESULT_PIC = 'result.bmp'


def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def lsb(bin_message, picture):
    x_size = picture.size[0]
    y_size = picture.size[1]

    bin_message = bin_message + ('0' * 8)

    for i in range(y_size):
        for j in range(x_size):
            pixel = picture.getpixel((j, i))
            if len(bin_message) > 3:
                new_pixel = embedding(pixel, bin_message[:3])
                bin_message = bin_message[3:]
                picture.putpixel((j, i), new_pixel)
                #picture.putpixel((j, i), (255,0, 0))
            else:
                new_pixel = embedding(pixel, bin_message)
                picture.putpixel((j, i), new_pixel)
                break
        if len(bin_message) < 3:
            break
    return picture

def embedding(pixel, bin_message):
    rgb = [pixel[0], pixel[1], pixel[2]]

    for i in range(len(bin_message)):
        channel_value = bin(pixel[i])
        channel_value = channel_value[:len(channel_value)-1] + bin_message[i]
        rgb[i] = int(channel_value, 2)
    return rgb[0], rgb[1], rgb[2]

def extract_message():
    picture = Image.open(RESULT_PIC)
    picture.load()

    x_size = picture.size[0]
    y_size = picture.size[1]
    secret_message = ''
    message_extracted = False

    for i in range(y_size):
        for j in range(x_size):
            pixel = picture.getpixel((j, i))
            secret_message = extract_bits_from_pixel(pixel, secret_message)
            if (len(secret_message) % 8 == 0) and (secret_message[-8:] == ('0' * 8)):
                secret_message = secret_message[:-8]
                message_extracted = True
                break
        if message_extracted:
            break

    secret_message = bin_to_str(secret_message)

    return secret_message

def extract_bits_from_pixel(pixel, secret_message):
    for i in range(len(pixel)):
        channel_value = bin(pixel[i])
        secret_message += channel_value[- 1]
        if (len(secret_message) % 8 == 0) and (secret_message[-8:] == ('0' * 8)):
            break

    return secret_message

def bin_to_str(message):
    str_data = ''
    for i in range(0, len(message), 8):
        temp_data = int(message[i:i + 8], 2)
        str_data += chr(temp_data)
    return str_data

def str_to_bin(message):
    result = ''.join(format(ord(x), 'b').zfill(8) for x in message)
    return result

def main():
    embedded_word_1 = "There"
    embedded_word_5 = "There was no possibility of"
    embedded_word_10 = "There was no possibility of taking a walk that day."
    embedded_word_20 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
                       "leafless shrubbery an"
    embedded_word_30 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
                       "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when"
    embedded_word_40 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
                       "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no " \
                       "company, dined early) the cold winter wind"
    embedded_word_50 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
                       "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no " \
                       "company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so " \
                       "penetrating."
    message_list = [embedded_word_1, embedded_word_5, embedded_word_10, embedded_word_20, embedded_word_30,
                    embedded_word_40, embedded_word_50]
    image_list = ['1.bmp', '2.bmp', '3.bmp']

    for image in image_list:
        print("Picture: {}".format(image))
        i = 1
        pic = Image.open(image)
        pic.load()
        for message in message_list:
            print("{}. Message: {}".format(i, message))

            bin_message = str_to_bin(message=message)
            new_image = lsb(bin_message=bin_message, picture=pic)

            new_image.save(RESULT_PIC)

            extracted_message = extract_message()

            print("   Extracted message: {}".format(extracted_message))
            if message == extracted_message:
                print(colored("   Message extracted succesfully!", "green"))
            else:
                print(colored("   Extraction ERROR!", "red"))

            original = cv2.imread(image)
            compressed = cv2.imread(RESULT_PIC)
            value = PSNR(original, compressed)
            print(f"   PSNR value is {value} dB")
            print()
            i += 1

    print("Check extraction after attack")

    pic = Image.open(RESULT_PIC)
    pic.load()

    extracted_message = extract_message()

    print("Message: {}".format(message_list[-1]))
    print("Extracted message:")
    print(extracted_message)

    if message_list[-1] == extracted_message:
        print(colored("   Message extracted succesfully!", "green"))
    else:
        print(colored("   Extraction ERROR!", "red"))

    return


if __name__ == '__main__':
    main()