import numpy as np
import cv2
from math import sqrt, log10


def psnr(original, compressed):
    mse = np.mean((original - compressed) ** 2)

    if(mse == 0):
        return 100

    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))

    return psnr


def get_video_psnr(original_video, compressed_video):
    psnr_sum = 0

    orig_video_capture = cv2.VideoCapture(original_video)
    compressed_video_capture = cv2.VideoCapture(compressed_video)

    total_frames = int(orig_video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    while True:
        ret, frame_orig = orig_video_capture.read()
        ret, frame_res = compressed_video_capture.read()

        if cv2.waitKey(1) & 0xFF == ord('q') or ret == False:
            orig_video_capture.release()
            compressed_video_capture.release()
            break

        psnr_sum += psnr(original=frame_orig, compressed=frame_res)

    average_psnr = psnr_sum / total_frames

    return average_psnr