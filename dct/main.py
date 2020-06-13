import cv2
from math import sqrt, log10
import numpy as np
import random

RESULT_PIC = "result.bmp"

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def RMSE(oroginal, compressed):
    rmse = np.sqrt(np.mean(np.square(oroginal - compressed)))
    return rmse


def bin_to_str(message):
    str_data = ''
    for i in range(0, len(message), 8):
        temp_data = int(message[i:i + 8], 2)
        str_data += chr(temp_data)
    return str_data


def str_to_bin(message):
    result = ''.join(format(ord(x), 'b').zfill(8) for x in message)
    return result


class ImageDCT():
    def __init__(self, image):
        self.B = 8
        self.image = image
        self.image_height = image.shape[0]
        self.image_width = image.shape[1]
        self.blocks_vertical = int(image.shape[0] / self.B)
        self.blocks_horizontal = int(image.shape[1] / self.B)
        self.dct_blocks = []

    def get_channel_matrix(self, channel_index):
        matrix = np.zeros((self.image_height, self.image_width), np.float64)
        for i in range(self.image_height):
            for j in range(self.image_width):
                matrix[i][j] = self.image[i][j][channel_index]
        return matrix

    def insert_channel_to_image(self, channel, channel_index):
        for i in range(self.image_height):
            for j in range(self.image_width):
                 self.image[i][j][channel_index] = channel[i][j]

        return

    def image_dct(self, channel_index):
        vis0 = np.zeros((self.image_height, self.image_width), np.float64)
        Trans = np.zeros((self.image_height, self.image_width), np.float64)
        vis0[:self.image_height, :self.image_width] = self.get_channel_matrix(channel_index=channel_index)

        for row in range(self.blocks_vertical):
            for col in range(self.blocks_horizontal):
                current_block = cv2.dct(vis0[row * self.B:(row + 1) * self.B, col * self.B:(col + 1) * self.B])
                self.dct_blocks.append(current_block)
                Trans[row * self.B:(row + 1) * self.B, col * self.B:(col + 1) * self.B] = current_block

        return

    def image_idct(self, channel_index):
        i = 0
        channel = np.zeros((self.image_height, self.image_width), np.float64)
        for row in range(self.blocks_vertical):
            for col in range(self.blocks_horizontal):
                current_block = cv2.idct(self.dct_blocks[i])
                channel[row * self.B:(row + 1) * self.B, col * self.B:(col + 1) * self.B] = current_block
                i += 1

        self.insert_channel_to_image(channel, channel_index)

        return


def lsb_of_dct(dct_blocks, bin_message, x, y):

    for i in range(len(bin_message)):
        whole_part, dec_part = str(dct_blocks[i][y][x]).split(".")
        coeff = bin(int(whole_part))
        coeff = coeff[coeff.index("b")+1:]

        coeff = (coeff[:-1] + bin_message[i])
        coeff = str(int(coeff, 2)) + "." + dec_part
        if whole_part[0] == '-':
            dct_blocks[i][y][x] = np.float64(coeff) * (-1)
        else:
            dct_blocks[i][y][x] = np.float64(coeff)

        if y == 0 and x == 0:
            dct_blocks[i][y][x] = dct_blocks[i][y][x] / 2

    return


def retrieve_message(dct_blocks, x, y):
    bin_message = ''
    for i in range(len(dct_blocks)):
        whole_part, dec_part = str(dct_blocks[i][y][x]).split(".")
        bit = bin(int(whole_part))[-1]
        bin_message += bit
        if (len(bin_message) % 8 == 0) and (bin_message[-8:] == ('0' * 8)):
            break

    return bin_message


def hide_message_len(bin_message, image):

    message_len = str_to_bin(str(len(bin_message))) + ('0' * 8)
    hidden = False

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel = image[j][i][2]
            channel_value = bin(pixel)
            channel_value = channel_value[:len(channel_value) - 1] + message_len[0]
            pixel = int(channel_value, 2)
            image[j][i][2] = pixel
            if len(message_len) == 1:
                hidden = True
                break
            message_len = message_len[1:]
        if hidden:
            break

    return


def extract_message_len(image):

    message_len = ''
    extracted = False

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel = image[j][i][2]
            channel_value = bin(pixel)
            message_len += channel_value[- 1]
            if (len(message_len) % 8 == 0) and (message_len[-8:] == ('0' * 8)):
                extracted = True
                break
        if extracted:
            break
    return int(bin_to_str(message_len[:-8]))


def retrieve_message_ext(dct_blocks, message_len):
    bin_message = ''

    for n in range(message_len):
        zero_bit_count = 0
        one_bit_count = 0

        for i in range(len(dct_blocks[n])):
            for j in range(len(dct_blocks[n])):
                whole_part, dec_part = str(dct_blocks[n][i][j]).split(".")
                if bin(int(whole_part))[-1] == '0':
                    zero_bit_count += 1
                else:
                    one_bit_count += 1

        if zero_bit_count > one_bit_count:
            bin_message += '0'
        # elif zero_bit_count == one_bit_count:
        #     bin_message += str(random.randrange(0, 2))
        else:
            bin_message += '1'

    return bin_message


def calculate_error_rate(message, retrieved_message):
    error_count = 0
    rate = 0
    for i in range(len(message)):
        if message[i] != retrieved_message[i]:
            error_count +=1

    rate = (error_count /len(message)) * 100
    return rate


def print_coeffs(block1, block2, y, x):
    for i in range(len(block1)):
        print("{}. {} \t {}".format(i, block1[i][y][x], block2[i][y][x]))
    return


def embed_and_retrieve(embedded_word, image, y, x):
    bin_message = str_to_bin(message=embedded_word) + "0"*8

    dct = ImageDCT(image=image)
    dct.image_dct(channel_index=0)
    lsb_of_dct(dct_blocks=dct.dct_blocks, bin_message=bin_message, x=x, y=y)
    dct.image_idct(channel_index=0)

    cv2.imwrite('BackTransformed.bmp', dct.image)

    # retrieve
    new_image = cv2.imread('BackTransformed.bmp')
    dct_retr = ImageDCT(image=new_image)
    dct_retr.image_dct(channel_index=0)
    retrieved_msg = retrieve_message(dct_blocks=dct_retr.dct_blocks, x=x, y=y)
    str_msg = bin_to_str(retrieved_msg)

    rate = calculate_error_rate(embedded_word, str_msg)
    # print("Message: {}".format(embedded_word_1))
    print("Retrieved message: {}".format(str_msg))
    print("Rate symbol: {}%".format(rate))
    # print("Message: {}".format(bin_message))
    # print("Retrieved message: {}".format(retrieved_msg))
    rate = calculate_error_rate(bin_message, retrieved_msg)
    # print(str(rate)[:5])
    print("Rate bit: {}%".format(rate))
    return


def embed_and_retrieve_ext(embedded_word, image):
    # embed
    bin_message = str_to_bin(message=embedded_word)

    hide_message_len(bin_message, image)

    dct = ImageDCT(image=image)
    dct.image_dct(channel_index=0)
    for i in range(dct.B):
        for j in range(dct.B):
            lsb_of_dct(dct_blocks=dct.dct_blocks, bin_message=bin_message, x=i, y=j)
    dct.image_idct(channel_index=0)

    cv2.imwrite(RESULT_PIC, dct.image)

    # retrieve
    new_image = cv2.imread(RESULT_PIC)
    message_len = extract_message_len(new_image)
    dct_retr = ImageDCT(image=new_image)
    dct_retr.image_dct(channel_index=0)
    retrieved_msg = retrieve_message_ext(dct_blocks=dct_retr.dct_blocks, message_len=message_len)
    str_msg = bin_to_str(retrieved_msg)

    rate = calculate_error_rate(embedded_word, str_msg)

    rate = calculate_error_rate(bin_message, retrieved_msg)
    print("  Error rate bit: {}%".format('%.2f' % rate))

    return

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
    # message_list = [embedded_word_1, embedded_word_5, embedded_word_10, embedded_word_20, embedded_word_30,
    #                 embedded_word_40, embedded_word_50]
    message_list = [embedded_word_50]
    word_number = [1, 5, 10, 20, 30, 40, 50]
    bin_message = str_to_bin(message=embedded_word_1)

    # image_list = ['1.bmp', '2.bmp']
    image_list = ['1.bmp']

    for image_name in image_list:
        print("Picture: {}".format(image_name))
        i = 0
        for message in message_list:
            # print("  {} word in message:".format(word_number[i]))
            image = cv2.imread(image_name)
            embed_and_retrieve_ext(message, image)

            original_img = cv2.imread(image_name)
            result_img = cv2.imread(RESULT_PIC)
            psnr = PSNR(original_img, result_img)
            rmse = RMSE(original_img, result_img)
            print("  PSNR: {} dB".format('%.2f' % psnr))
            print("  RMSE: {}".format('%.2f' % rmse))
            print()
            i += 1


    return


if __name__ == "__main__":
    main()
