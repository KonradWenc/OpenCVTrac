# Imports
import Common
import cv2 as opencv


class CameraCapture:
    # Preview
    is_preview_active = False

    # Reference rectangle selected by user
    user_rectangle = None

    def __init__(self):
        # Init camera
        self.camera_capture = opencv.VideoCapture(0)

        # Get fps and calculate delay
        fps = self.camera_capture.get(opencv.CAP_PROP_FPS)
        self.ms_delay = int(1000 / fps)

        # Initialize windows
        opencv.namedWindow(Common.preview_window_name, opencv.WINDOW_KEEPRATIO)

        # Set mouse callback
        opencv.setMouseCallback(Common.preview_window_name, self.on_mouse_move)

    def start_preview(self):
        self.is_preview_active = True

        while self.is_preview_active:
            self.capture_and_display_frame()

    def stop_preview(self):
        self.is_preview_active = False

    def capture_and_display_frame(self):
        # Read frame from the camera
        (capture_status, self.current_camera_frame) = self.camera_capture.read()

        # Verify capture status
        if capture_status:
            self.draw_user_rectangle()

            # Display the captured frame
            opencv.imshow(Common.preview_window_name, self.current_camera_frame)

            # Check, whether user pressed 'q' key
            if opencv.waitKey(self.ms_delay) == Common.quit_key:
                self.stop_preview()
        else:
            # Print error to the console
            print(Common.capture_failed)

    def draw_user_rectangle(self):
        if self.user_rectangle is not None:
            top_left_corner = (self.user_rectangle[0], self.user_rectangle[1])
            bottom_right_corner = (self.user_rectangle[2], self.user_rectangle[3])

            opencv.rectangle(self.current_camera_frame, top_left_corner, bottom_right_corner,
                             Common.yellow, Common.rectangle_thickness)

    def release(self):
        # Stop and release camera preview
        self.stop_preview()
        self.camera_capture.release()

        # Release all windows
        opencv.destroyAllWindows()

    def on_mouse_move(self, event, x, y, flags, user_data):
        # Left mouse button pressed and started drawing the rectangle
        if event == opencv.EVENT_LBUTTONDOWN:
            self.mouse_start_pos = (x, y)

        # Event - Drawing the rectangle
        # We store coords of this rectangle in the user_rectangle field
        elif (flags & opencv.EVENT_FLAG_LBUTTON):
            if self.mouse_start_pos is not None:
                min_pos = min(self.mouse_start_pos[0], x), min(self.mouse_start_pos[1], y)
                max_pos = max(self.mouse_start_pos[0], x), max(self.mouse_start_pos[1], y)

                self.user_rectangle = (min_pos[0], min_pos[1], max_pos[0], max_pos[1])

        # Event - finished drawing the rectangle
        elif event == opencv.EVENT_LBUTTONUP:
            self.mouse_start_pos = None

        # Event - Reset the rectangle
        elif event == opencv.EVENT_RBUTTONDOWN | opencv.EVENT_LBUTTONDBLCLK | opencv.EVENT_MBUTTONDBLCLK:
            self.user_rectangle = None
