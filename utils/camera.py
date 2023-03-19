import subprocess
import cv2

def open_cam_onboard(width, height):
    """Open the Jetson onboard camera."""
    gst_elements = str(subprocess.check_output('gst-inspect-1.0'))
    if 'nvcamerasrc' in gst_elements:
        # On versions of L4T prior to 28.1, you might need to add
        # 'flip-method=2' into gst_str below.
        gst_str = f'nvcamerasrc ! '\
                   'video/x-raw(memory:NVMM), '\
                   'width=1280, height=720, '\
                   'format=I420, framerate=60/1 ! '\
                   'nvvidconv ! '\
                   f'video/x-raw, width={width[0]}, height={height[0]}, '\
                   'format=BGRx ! '\
                   'videoconvert ! appsink'
    elif 'nvarguscamerasrc' in gst_elements:
        gst_str = 'nvarguscamerasrc ! '\
                   'video/x-raw(memory:NVMM), '\
                   'width=3264, height=2464, '\
                   'format=NV12, framerate=21/1 ! '\
                   'nvvidconv flip-method=2 ! '\
                   f'video/x-raw, width={width[0]}, height={height[0]}, '\
                   'format=BGRx ! '\
                   'videoconvert ! appsink'
    else:
        raise RuntimeError('onboard camera source not found!')
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)


