from dct import ImageDCT

import numpy as np
import cv2
import math


class MessageEmbedder:
    def __init__(self, coder_decoder, video):
        self.bin_message = ''
        self.video_container = video
        self.coder = coder_decoder
        self.video_height = int(self.video_container.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_width = int(self.video_container.get(cv2.CAP_PROP_FRAME_WIDTH))

    def embed_to_container(self, message):

        frames_number = int(self.video_container.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = self.video_container.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        result_video = cv2.VideoWriter('output.mp4', fourcc, fps, (self.video_width, self.video_height))

        ret, frame = self.video_container.read()

        encoded_message = self.coder.encode_message(message_sequence=[ord(x) for x in message])
        self.bin_message = self.coder.message_seq_to_bin_str(message=encoded_message)

        while True:

            if cv2.waitKey(1) & 0xFF == ord('q') or ret == False:
                self.video_container.release()
                break

            if len(self.bin_message) == 0:
                if len(self.coder.rest_of_message) != 0:
                    encoded_message = self.coder.encode_message(message_sequence=self.coder.rest_of_message)
                    self.bin_message = self.coder.message_seq_to_bin_str(message=encoded_message)

            if len(self.bin_message) != 0:
                frame = self.embed_to_frame(frame=frame)

            result_video.write(frame)

            ret, frame = self.video_container.read()

        result_video.release()

        cv2.destroyAllWindows()

        return

    def embed_to_frame(self, frame):

        frameYCrCb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)

        dct = ImageDCT(frameYCrCb)
        dct.image_dct(channel_index=0)

        # self.lsb_of_dct(dct_blocks=dct.dct_blocks, x=6, y=6)
        self.embed_to_high_freq(dct_blocks=dct.dct_blocks)
        dct.image_idct(channel_index=0)

        frame = cv2.cvtColor(dct.image, cv2.COLOR_YCR_CB2BGR)

        return frame

    def embed_to_high_freq(self, dct_blocks):

        for i in range(len(dct_blocks)):

            if self.bin_message[0] == '0':
                dct_blocks[i][7][7] = 15
            else:
                dct_blocks[i][7][7] = -15

            if len(self.bin_message) == 1:
                self.bin_message = ''
                break

            self.bin_message = self.bin_message[1:]

        return

    # with RS-codes
    # def embed_to_high_freq(self, dct_blocks):
    #
    #     for i in range(len(dct_blocks)):
    #
    #         whole_part, dec_part = str(dct_blocks[i][7][7]).split(".")
    #         coeff_value = str(self.bin_message[0]) + "." + dec_part
    #
    #         if whole_part[0] == '-':
    #             dct_blocks[i][7][7] = np.float64(coeff_value) * (-1)
    #         else:
    #             dct_blocks[i][7][7] = np.float64(coeff_value)
    #
    #         if len(self.bin_message) == 1:
    #             self.bin_message = []
    #             break
    #
    #         self.bin_message = self.bin_message[1:]
    #
    #     return

    def lsb_of_dct(self, dct_blocks, x, y):
        for i in range(len(dct_blocks)):
            whole_part, dec_part = str(dct_blocks[i][y][x]).split(".")
            coeff = bin(int(whole_part))
            coeff = coeff[coeff.index("b") + 1:]

            coeff = (coeff[:-1] + self.bin_message[0])
            coeff = str(int(coeff, 2)) + "." + dec_part
            if whole_part[0] == '-':
                dct_blocks[i][y][x] = np.float64(coeff) * (-1)
            else:
                dct_blocks[i][y][x] = np.float64(coeff)

            if len(self.bin_message) == 1:
                self.bin_message = ''
                break

            self.bin_message = self.bin_message[1:]

        return

    # def hide_message_len(self, image):
    #     message_len = Converter.str_to_bin(str(len(self.bin_message))) + ('0' * 8)
    #     hidden = False
    #
    #     for i in range(self.video_height):
    #         for j in range(self.video_width):
    #             pixel = image[i][j][2]
    #             channel_value = bin(pixel)
    #             channel_value = channel_value[:len(channel_value) - 1] + message_len[0]
    #             pixel = int(channel_value, 2)
    #             image[i][j][2] = pixel
    #             if len(message_len) == 1:
    #                 hidden = True
    #                 break
    #             message_len = message_len[1:]
    #         if hidden:
    #             break
    #
    #     return

    def is_possible_to_embed(self):
        frames_number = int(self.video_container.get(cv2.CAP_PROP_FRAME_COUNT))
        video_height = self.video_container.get(cv2.CAP_PROP_FRAME_HEIGHT)
        video_width = self.video_container.get(cv2.CAP_PROP_FRAME_WIDTH)
        blocks_per_frame = math.floor(video_height / 8) * math.floor(video_width / 8)
        max_bit_num = blocks_per_frame * frames_number

        if len(self.bin_message) <= max_bit_num:
            return True
        else:
            return False
