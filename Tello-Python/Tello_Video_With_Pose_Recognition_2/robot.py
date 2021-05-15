import cv2

from GUI import GUI
from ai import AI
from pose import Pose


class Robot:
    def __init__(self, drone, camera):
        self.frame = None
        self.main = None
        self.stop_event = None

        self.gui = GUI()
        self.ai = AI()
        self.pose = Pose()
        self.camera = camera
        self.drone = drone

    def start(self):
        # get first frame
        frame = self.camera.get_frame()

        # main loop
        while True:
            # initial setup
            if frame is not None:
                if self.gui.window_width is None or self.gui.center_box_points is None:
                    self.gui.set_window_size(frame, self.camera)
                    self.gui.get_center_box_points(frame)

                self.process_feed(self.pose, self.ai, self.gui, frame)

            # get next frame
            frame = self.camera.get_frame()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def process_feed(self, pose, ai, gui, frame):
        # each frame, run detection
        # each period, return the move likely pose
        current_pose, gui_skeleton_flag, points = pose.detect(frame)
        ai.update_current_pose(current_pose)

        ai.get_sum_of_distance(points, gui.center_point)
        ai.get_is_pose_in_box()

        ai.calculate_drone_cmd()

        gui.update_image(frame, gui_skeleton_flag, points, ai)

        ai.reset_state()
