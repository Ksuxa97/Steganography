import cv2
import numpy as np


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
