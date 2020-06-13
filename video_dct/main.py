import cv2
import random

from coder import CoderDecoder
from embedder import MessageEmbedder
from extractor import MessageExtractor
from psnr import get_video_psnr

VIDEO_CONTAINER = "0.20.mp4"


def main():
    
    print("1. Embed message")
    print("2. Retrieve message")
    print("3. Embed and retrieve message")
    print("4. Calculate PSNR")
    action_index = input("Plese, choose the action: ")

    if action_index == '1':
        embed_message_into_container()
    elif action_index == '2':
        retrieve_message_from_container()
    elif action_index == '3':
        emulate_message_transfer()
    elif action_index == '4':
        original = input("Please, enter the name of the original video: ")
        compressed = input("Please, enter the name of the compressed video: ")
        psnr = get_video_psnr(original_video=original, compressed_video=compressed)
        print("PSNR: {}".format(psnr))

    return


def embed_message_into_container():

    message = input("Please enter your message: ")
    container_name = input("Please, enter container name: ")

    coder_decoder = CoderDecoder()

    video_capture = cv2.VideoCapture(container_name)

    message_embedder = MessageEmbedder(coder_decoder=coder_decoder, video=video_capture)
    message_embedder.embed_to_container(message=message)


def retrieve_message_from_container():

    container = input("Please, enter container name: ")
    key = input("Please, enter key to retrieve message: ")

    message_len = extract_msg_len_from_key(key=key)

    coder_decoder = CoderDecoder()

    # retrieve
    video_capture = cv2.VideoCapture(container)

    message_extractor = MessageExtractor(coder_decoder=coder_decoder, video=video_capture)

    result_message = message_extractor.retrieve_message(message_len=message_len)

    return result_message


def emulate_message_transfer():

    print()
    print("Sender.")
    message = input("Please enter your message: ")
    coder_decoder = CoderDecoder()

    container_name = input("Please, enter container name: ")
    video_capture = cv2.VideoCapture(container_name)

    print("Generating access key....")
    key = generate_key(message=message)
    print("Secret key: {}".format(key))

    message_embedder = MessageEmbedder(coder_decoder=coder_decoder, video=video_capture)
    message_embedder.embed_to_container(message=message)
    print("Message is embedded!")
    print()

    # retrieve
    print("Recipient.")
    container_name = input("Please, enter container name: ")
    video_capture = cv2.VideoCapture(container_name)
    key = input("Please, enter key to retrieve message: ")

    msg_len = extract_msg_len_from_key(key=key)
    message_extractor = MessageExtractor(coder_decoder=coder_decoder, video=video_capture)
    result_message = message_extractor.retrieve_message(message_len=msg_len)

    print("Retrieved message is: {}".format(result_message))

    return


def autorun(message):

    coder_decoder = CoderDecoder()

    container_name = 'orig.mp4'
    video_capture = cv2.VideoCapture(container_name)

    message_embedder = MessageEmbedder(coder_decoder=coder_decoder, video=video_capture)
    message_embedder.embed_to_container(message=message)

    # retrieve
    container_name = 'output.mp4'
    video_capture = cv2.VideoCapture(container_name)

    msg_len = len(message)
    message_extractor = MessageExtractor(coder_decoder=coder_decoder, video=video_capture)
    result_message = message_extractor.retrieve_message(message_len=msg_len)

    return


def generate_key(message):

    right = random.randint(10, 100)
    left = random.randint(10, 100)
    x = len(message)

    str_key = str(left) + str(x) + str(right)
    x = int(str_key)

    return x


def extract_msg_len_from_key(key):
    msg_len = str(key)[2:-2]
    msg_len = int(msg_len)
    return msg_len


def PSNR_test():
    message1 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the "

    message2 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
               "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no "

    message3 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
               "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no " \
               "company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so "

    message4 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
               "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no " \
               "company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so " \
               "penetrating. Dorian is the grandson of the late Lord Kelso. His mother, Lady Margaret Devereux, was "

    message5 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
               "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no " \
               "company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so " \
               "penetrating. Dorian is the grandson of the late Lord Kelso. His mother, Lady Margaret Devereux, was " \
               "portrayed as a beautiful and rich woman. Her grandfather had a strong dislike for Kelso, and in turn, "

    message6 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
               "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no " \
               "company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so " \
               "penetrating. Dorian is the grandson of the late Lord Kelso. His mother, Lady Margaret Devereux, was " \
               "portrayed as a beautiful and rich woman. Her grandfather had a strong dislike for Kelso, and in turn, " \
               "Margaret received the entire Selby property. Dorian' \s father, a subaltern in a foot regiment, was killed"

    message7 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
               "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no " \
               "company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so " \
               "penetrating. Dorian is the grandson of the late Lord Kelso. His mother, Lady Margaret Devereux, was " \
               "portrayed as a beautiful and rich woman. Her grandfather had a strong dislike for Kelso, and in turn, " \
               "Margaret received the entire Selby property. Dorian' \s father, a subaltern in a foot regiment, was killed" \
               " by a Belgian brute a few months after his marriage to Lady Margaret, who died soon after. The "

    message8 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
               "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no " \
               "company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so " \
               "penetrating. Dorian is the grandson of the late Lord Kelso. His mother, Lady Margaret Devereux, was " \
               "portrayed as a beautiful and rich woman. Her grandfather had a strong dislike for Kelso, and in turn, " \
               "Margaret received the entire Selby property. Dorian' \s father, a subaltern in a foot regiment, was killed" \
               " by a Belgian brute a few months after his marriage to Lady Margaret, who died soon after. The " \
               "Reed-Solomon code properties discussed above make them especially well-suited to applications where "

    message9 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
               "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no " \
               "company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so " \
               "penetrating. Dorian is the grandson of the late Lord Kelso. His mother, Lady Margaret Devereux, was " \
               "portrayed as a beautiful and rich woman. Her grandfather had a strong dislike for Kelso, and in turn, " \
               "Margaret received the entire Selby property. Dorian' \s father, a subaltern in a foot regiment, was killed" \
               " by a Belgian brute a few months after his marriage to Lady Margaret, who died soon after. The " \
               "Reed-Solomon code properties discussed above make them especially well-suited to applications where " \
               "errors occur in bursts. This is because it does not matter to the code how many bits in a symbol are in "

    message10 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
                "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no " \
                "company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so " \
                "penetrating. Dorian is the grandson of the late Lord Kelso. His mother, Lady Margaret Devereux, was " \
                "portrayed as a beautiful and rich woman. Her grandfather had a strong dislike for Kelso, and in turn, " \
                "Margaret received the entire Selby property. Dorian' \s father, a subaltern in a foot regiment, was killed" \
                " by a Belgian brute a few months after his marriage to Lady Margaret, who died soon after. The " \
                "Reed-Solomon code properties discussed above make them especially well-suited to applications where " \
                "errors occur in bursts. This is because it does not matter to the code how many bits in a symbol are in " \
                "error - if multiple bits in a symbol are corrupted it only counts as a single error. Conversely, if a "

    message11 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
                "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no " \
                "company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so " \
                "penetrating. Dorian is the grandson of the late Lord Kelso. His mother, Lady Margaret Devereux, was " \
                "portrayed as a beautiful and rich woman. Her grandfather had a strong dislike for Kelso, and in turn, " \
                "Margaret received the entire Selby property. Dorian' \s father, a subaltern in a foot regiment, was killed" \
                " by a Belgian brute a few months after his marriage to Lady Margaret, who died soon after. The " \
                "Reed-Solomon code properties discussed above make them especially well-suited to applications where " \
                "errors occur in bursts. This is because it does not matter to the code how many bits in a symbol are in " \
                "error - if multiple bits in a symbol are corrupted it only counts as a single error. Conversely, if a " \
                "data stream is not characterized by error bursts or drop-outs but by random single bit errors, a "

    message12 = "There was no possibility of taking a walk that day. We had been wandering, indeed, in the " \
                "leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no " \
                "company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so " \
                "penetrating. Dorian is the grandson of the late Lord Kelso. His mother, Lady Margaret Devereux, was " \
                "portrayed as a beautiful and rich woman. Her grandfather had a strong dislike for Kelso, and in turn, " \
                "Margaret received the entire Selby property. Dorian' \s father, a subaltern in a foot regiment, was killed" \
                " by a Belgian brute a few months after his marriage to Lady Margaret, who died soon after. The " \
                "Reed-Solomon code properties discussed above make them especially well-suited to applications where " \
                "errors occur in bursts. This is because it does not matter to the code how many bits in a symbol are in " \
                "error - if multiple bits in a symbol are corrupted it only counts as a single error. Conversely, if a " \
                "data stream is not characterized by error bursts or drop-outs but by random single bit errors, a " \
                "Reed-Solomon code is usually a poor choice compared to a binary code."

    messages = [message1, message2, message3, message4, message5, message6, message7, message8, message9,
                message10, message11, message12]

    for i in range(len(messages)):
        autorun(message=messages[i])

        psnr = get_video_psnr(original_video='orig.mp4', compressed_video='output.mp4')
        print("{}. Symbols: {}, PSNR: {}".format(i + 1, len(messages[i]), psnr))

    return


if __name__ == "__main__":
    main()
