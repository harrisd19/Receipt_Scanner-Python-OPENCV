def bgr2rgb(im):
    """
    Converts image from BGR (blur, green, red) to RGB. OpenCV use BGR instead of RGB in some cases,
    however RGB is the standard for matplotlib.
    """
    from cv2 import cvtColor, COLOR_BGR2RGB
    return cvtColor(im, COLOR_BGR2RGB)

def run_video(process_frame=lambda im:im, fps=30, camera_num=0):
    """
    Runs OpenCV video from a connected camera as Jupyter notebook output. Each frame from the camera
    is given to process_frame before being displayed. The default does no processing. The display is
    limited to the given number of frames per second (default 30). It can go below this, but will
    bot go above it. If there is more than one camera connected, settings camera_num will select
    which camera to use.
    
    The video will continue being run until the code is interuppted with the stop button in Jupyter
    notebook.
    """
    from cv2 import VideoCapture, error, imencode
    from IPython.display import Image, display
    from time import time, sleep
    delay = 1/fps # the max number of seconds between frames
    vc = VideoCapture(camera_num)
    try:
        if not vc.isOpened(): return # if we did not successfully gain access to the camera
        # Try to get the first frame
        is_capturing, frame = vc.read()
        if frame is None: return # no first frame
        # Process the frame, encode it as PNG, and display it
        im = process_frame(bgr2rgb(frame))
        disp = display(Image(imencode('.jpg', bgr2rgb(im))[1].tostring(), width=im.shape[1], height=im.shape[0]), display_id=True)
        while is_capturing:
            # Keep getting new frames while they are available
            try:
                start = time()
                # Get the next frame
                is_capturing, frame = vc.read()
                if frame is None: break # no next frame
                # Process the frame, encode it as PNG, and display it
                im = process_frame(bgr2rgb(frame))
                disp.update(Image(imencode('.jpg', bgr2rgb(im))[1].tostring(), width=im.shape[1], height=im.shape[0]))
                # Wait for a small amount of time to avoid frame rate going to high
                wait = delay - (time() - start)
                if wait > 0: sleep(wait)
            except KeyboardInterrupt: break # lookout for a keyboard interrupt (stop button) to stop the script gracefully
        return im
    finally: vc.release()
    return None
