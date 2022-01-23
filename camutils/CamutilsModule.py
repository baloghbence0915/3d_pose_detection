import cv2
import glob
import re
from os.path import join
from fileutils.FileUtilsModule import getAbsolutePath

# Source: https://stackoverflow.com/a/47248339/11436145


def rotate_image(mat, angle):
    """
    Rotates an image (angle in degrees) and expands image to avoid cropping
    """

    height, width = mat.shape[:2]  # image shape has 3 dimensions
    # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
    image_center = (width/2, height/2)

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat


RECORDING_DIR = 'recordings'


def get_path_of_recoding(session_name, channel):
    return join(RECORDING_DIR, session_name + '_ch_{0}.avi'.format(channel))


def get_recordings():
    path = join(RECORDING_DIR, '*.avi')
    recordings = glob.glob(path)
    recordings = [r.split('\\').pop() for r in recordings]
    recordings = [re.sub('_ch_[0-9]*.avi', '', r) for r in recordings]
    recordings = list(dict.fromkeys(recordings))
    return recordings
