# Imports
import Common
import cv2 as opencv


class CameraCapture:
    # Preview
    is_preview_active = False

    def __init__(self):
        # Init camera
        self.camera_capture = opencv.VideoCapture(0)

        # Get fps and calculate delay
        fps = self.camera_capture.get(opencv.CAP_PROP_FPS)
        self.ms_delay = int(1000 / fps)

        # Initialize windows
        opencv.namedWindow(Common.preview_window_name, opencv.WINDOW_FREERATIO)

    def start_preview(self):
        self.is_preview_active = True

        while(self.is_preview_active):
            self.capture_and_display_frame()

    def stop_preview(self):
        self.is_preview_active = False

    def capture_and_display_frame(self):

        # Read frame from the camera
        (capture_status, self.current_camera_frame) = self.camera_capture.read()

        # Verify capture status
        if(capture_status):

            # Display the captured frame
            opencv.imshow(Common.preview_window_name, self.current_camera_frame)

            # Check, whether user pressed 'q' key
            if(opencv.waitKey(self.ms_delay) == Common.quit_key):
                self.stop_preview()

        else:
            # Print error to the console
            print(Common.capture_failed)

    def release(self):
        # Stop and release camera preview
        self.stop_preview()
        self.camera_capture.release()

        # Release all windows
        opencv.destroyAllWindows()