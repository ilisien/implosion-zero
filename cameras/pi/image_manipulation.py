import numpy as np, cv2
from PIL import Image
from globals import ImageType, ImageSizePreset, FRAME_RES

def rgb565_to_rgb(byte1, byte2):
    r = ((byte1 & 0xF8) >> 3) << 3
    g = (((byte1 & 0x07) << 3) | ((byte2 & 0xE0) >> 5)) << 2
    b = (byte2 & 0x1F) << 3
    return r, g, b

def image_from_bytes(image_type,image_size_preset,image_bytes):
    width, height = FRAME_RES[image_size_preset]
    if image_type == ImageType.RGB565: # color image
        image_data = np.zeros((height, width, 3), dtype=np.uint8)
        byte_index = 0

        for y in range(height):
            for x in range(width):
                byte1 = image_bytes[byte_index]
                byte2 = image_bytes[byte_index + 1]
                r, g, b = rgb565_to_rgb(byte1, byte2)
                image_data[y, x] = [b, g, r]  # OpenCV uses BGR format

                byte_index += 2
        return image_data
    if image_type == ImageType.GRAYSCALE: # grayscale image
        pass # todo