import cv2

from dct import ImageDCT

class MessageExtractor:

    def __init__(self, coder_decoder, video):
        self.decoder = coder_decoder
        self.video_container = video
        self.video_height = int(self.video_container.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_width = int(self.video_container.get(cv2.CAP_PROP_FRAME_WIDTH))

    def retrieve_message(self, message_len):

        message = ''
        bits_per_block = 255 * 8
        bin_message = ''

        while len(message) < message_len:
            ret, frame = self.video_container.read()
            frameYCrCb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)

            dct_retr = ImageDCT(image=frameYCrCb)
            dct_retr.image_dct(channel_index=0)

            bin_message = self.retrieve_message_from_frame(dct_blocks=dct_retr.dct_blocks, message_len=bits_per_block)

            message_seq = self.decoder.bin_str_to_msg_seq(message=bin_message)
            decoded_message = self.decoder.decode_message(message_sequence=message_seq)
            message = message + ''.join(chr(x) for x in decoded_message)

        return message


    @staticmethod
    def retrieve_message_from_frame(dct_blocks, message_len):
        bin_message = ''
        for i in range(len(dct_blocks)):
            if dct_blocks[i][7][7] < 0:
                bin_message += '1'
            else:
                bin_message += '0'

            if len(bin_message) == message_len:
                break

        return bin_message


