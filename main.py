
import cv2
import time
from datetime import datetime
import os
import argparse
import threading
from imutils.video.videostream import  VideoStream
from utils import server
import subprocess
import pdb

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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str,
                    help="path to optional output video file")
    ap.add_argument("-i", "--input", type=str,
                    help="path to optional output video file")
    ap.add_argument("-u", "--use-pi-camera",
                    help="use an rpi camera")
    ap.add_argument("-b", "--bottle-server", action="store_true",
                    help="enable a local bottle server to stream images")
    ap.add_argument("-r", "--resolution", type=tuple, default=(320, 480),
                    help="Set stream resolution")
    args = vars(ap.parse_args())

    if args["bottle_server"] is not None:
        t = threading.Thread(target=server.serve, args=())
        t.daemon = True
        t.start()

    writer = None
    sensor_id=1,
    capture_width=960,
    capture_height=540,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
    #vs = cv2.VideoCapture(
    #    "nvgstcapture-1.0 --orientation=2"
    #    )
    vs = open_cam_onboard(capture_width, capture_height)

    while True:
        frame = vs.read()[1]
        #frame = frame[1] if args["input"] is not None else frame
        # if we are viewing a video and we did not grab a frame then we
        # have reached the end of the video
        if args["input"] is not None and frame is None:
            break

        if writer is None and args["output"] is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H:%M:%S")
            filename = "{}_vanilla.avi".format(timestamp)
            output_path = os.path.join(args["output"], filename)

            (H, W) = frame.shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter(output_path, fourcc, 30, (W, H), True)

        if writer is not None:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            writer.write(rgb)

        if args["bottle_server"] is not None:
            with server.lock:
                server.streamedFrame = frame

    print("Shutting Down")
    vs.close()
    if writer is not None:
        writer.release()
