import cv2
import glob
import re
from os.path import join
from calculations.CalculationsModule import getBodyAngle, getDistanceOfPoint, getSpeed, linearFn, unwrapCoords
from fileutils.FileUtilsModule import getAbsolutePath

# Source: https://stackoverflow.com/a/47248339/11436145


def rotateImage(mat, angle):
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


def getPathOfRecoding(session_name, channel):
    return join(RECORDING_DIR, session_name + '_ch_{0}.avi'.format(channel))


def getRecordings():
    path = join(RECORDING_DIR, '*.avi')
    recordings = glob.glob(path)
    recordings = [r.split('\\').pop() for r in recordings]
    recordings = [re.sub('_ch_[0-9]*.avi', '', r) for r in recordings]
    recordings = list(dict.fromkeys(recordings))
    return recordings


def applyImageModifiers(frame, side, config, detector, undistortion):
    mods = config.get()['camera']['mods']
    rot = mods[side]['rot']
    undistortionEnabled = mods['all']['undistortion']['enabled']

    if undistortionEnabled:
        frame = undistortion.execute(frame)

    if rot > 0:
        frame = rotateImage(frame, rot * 90)

    pose = detector.getPose(frame)

    return (frame, pose)

def getKeyPoints(frames, poses, config):
    show_points_per_side = config.get(
    )['debug']['show_points_per_side']

    calculations = config.get()['calculations']
    stereo_baseline = calculations["stereo_baseline"]
    horizontal_angle = calculations["horizontal_angle"]
    stereo_scale = calculations["stereo_scale"]

    move_points_to_center = calculations["move_points_to_center"]
    offset = calculations["offset"]
    align_ground = calculations["align_ground"]
    normalize_height = calculations["normalize_height"]

    if move_points_to_center and offset['enabled']:
        raise Exception(
            'Cannot move points to the center and set offset the same time!')

    points = {"left": None, "right": None}
    resp = {"points": {}}
    ratio = 0

    for side, frame in frames.items():
        if frame is None:
            continue

        ratio = frame.shape[0] / frame.shape[1]

        pose = poses[side]

        if pose is not None:
            points[side] = {id: {'x': l.x, 'y': (
                1-l.y)*ratio} for id, l in enumerate(pose.landmark)}

    if points['left'] is not None and points['right'] is not None:
        # difference from X and Z axis
        diffX = 0
        diffZ = 0
        # 11 - left_shoulder ; 12 - right_shoulder
        for i in [11, 12]:
            leftX, _, rightX, _ = unwrapCoords(points, i)
            diffX += (leftX + rightX)/2
            diffZ += getDistanceOfPoint(leftX, rightX,
                                        horizontal_angle, stereo_baseline, stereo_scale)
        diffX /= 2
        diffZ /= 2

        algGround = 0
        if align_ground['enabled']:
            algGround = linearFn(
                diffZ, align_ground['slope'], align_ground['bias'])

        normHeight = 1
        if normalize_height['enabled']:
            normHeight = linearFn(
                diffZ, normalize_height['slope'], normalize_height['bias'])

        for i in range(33):
            leftX, leftY, rightX, rightY = unwrapCoords(points, i)

            x = (leftX+rightX)/2
            y = (leftY+rightY)/2
            z = getDistanceOfPoint(
                leftX, rightX, horizontal_angle, stereo_baseline, stereo_scale)

            #
            if align_ground['enabled']:
                y += algGround

            #
            if move_points_to_center:
                x -= diffX
                z -= diffZ

            #
            if normalize_height['enabled']:
                if not move_points_to_center:
                    x -= diffX
                    z -= diffZ
                x *= normHeight
                y *= normHeight
                z *= normHeight
                if not move_points_to_center:
                    x += diffX
                    z += diffZ

            #
            if offset['enabled']:
                x += offset['x']
                z += offset['z']

            resp["points"][i] = {'x': 1-x, 'y': y, 'z': z}

    resp['angle'] = getBodyAngle(resp['points'])
    resp['speed'] = getSpeed(resp['points'])

    resp['debug'] = {'ratio': ratio}

    if show_points_per_side:
        resp['debug']['left'] = points['left']
        resp['debug']['right'] = points['right']

    return resp