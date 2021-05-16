import cv2
import time
import threading

from GUI import GUI
from ai import AI
from pose import Pose


class Robot:
    def __init__(self, drone, camera):
        self.frame = None
        self.main = None
        self.stop_event = None
        self.distance = 1  # default distance for 'move' cmd
        self.degree = 30  # default degree for 'cw' or 'ccw' cmd

        self.gui = GUI()
        self.ai = AI()
        self.pose = Pose()
        self.camera = camera
        self.drone = drone

        self.auto_takeoff_thread = threading.Thread(target=self._autoTakeoff)
        self.sending_command_thread = threading.Thread(target=self._sendingCommand)

    def start(self):
        # get first frame
        frame = self.camera.get_frame()

        # main loop
        while True:
            # initial setup
            if frame is not None:
                if self.gui.window_width is None or self.gui.center_box_points is None:
                    self.gui.set_window_size(frame)
                    self.gui.get_center_box_points(frame)

                self.process_feed(self.pose, self.ai, self.gui, frame)

            # get next frame
            frame = self.camera.get_frame()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.on_close()
                break

    def process_feed(self, pose, ai, gui, frame):
        # each frame, run detection
        # each period, return the move likely pose
        current_pose, gui_skeleton_flag, points = pose.detect(frame)
        ai.update_current_pose(current_pose)

        ai.get_sum_of_distance(points, gui.center_point)
        ai.get_is_pose_in_box()

        ai.get_center_human_cmd()

        gui.update_image(frame, gui_skeleton_flag, points, ai)

        # handle human seeking
        if ai.drone_cmd == 'x-dec':
            self.telloMoveLeft()
        elif ai.drone_cmd == 'x-inc':
            self.telloMoveRight()
        elif ai.drone_cmd == 'y-inc':
            self.telloUp()
        elif ai.drone_cmd == 'y-dec':
            self.telloDown()

        # handle pose cmds
        if ai.current_pose == 'left_arm_flat':
            self.telloTakeOff()
        elif ai.current_pose == 'right_arm_flat':
            self.telloLanding()

        ai.reset_state()

    def _sendingCommand(self):
        """
        start a while loop that sends 'command' to tello every 5 second
        """

        while True:
            self.drone.send_command('command')
            time.sleep(5)

    def _autoTakeoff(self):
        """
        Firstly,it will waiting for the response that will be sent by Tello if Tello

        finish the takeoff command.If computer doesn't receive the response,it may be

        because tello doesn't takeoff normally,or because the UDP pack of response is

        lost.So in order to confirm the reason,computer will send 'height?'command to

        get several real-time height datas and get a average value.If the height is in

        normal range,tello will execute the moveup command.Otherwise,tello will land.

        Finally,the sending-command thread will start.
        """
        response = None
        height_tmp = 0  # temp variable to content value of height
        height_val = 0  # average value of height
        cnt = 0  # effective number of height reading
        timeout = 6  # max waiting time of tello's response

        # waiting for the response from tello
        while response != 'ok':
            # if self.quit_waiting_flag is True:
            #     break
            response = self.drone.get_response()
            print "ack:%s" % response

        # receive the correct response
        if response == 'ok':
            self.drone.move_up(0.5)

        # calculate the height of drone
        else:
            for i in range(0, 50):
                height_tmp = self.drone.get_height()
                try:
                    height_val = height_val + height_tmp
                    cnt = cnt + 1
                    print height_tmp, cnt
                except:
                    height_val = height_val

            height_val = height_val / cnt

            # if the height value is in normal range
            if height_val == 9 or height_val == 10 or height_val == 11:
                self.drone.move_up(0.5)
            else:
                self.drone.land()
        # start the sendingCmd thread
        self.sending_command_thread.start()

    def telloTakeOff(self):
        """
        send the takeoff command to tello,and wait for the first response,

        if get the 'error'response,remind the "battery low" warning.Otherwise,

        start the auto-takeoff thread
        """
        takeoff_response = None

        self.drone.takeoff()
        time.sleep(0.2)

        takeoff_response = self.drone.get_response()

        if takeoff_response != 'error':
            self.auto_takeoff_thread.start()
        else:
            print "battery low,please repalce with a new one"

    def telloLanding(self):
        return self.drone.land()

    def telloFlip_l(self):
        return self.drone.flip('l')

    def telloFlip_r(self):
        return self.drone.flip('r')

    def telloFlip_f(self):
        return self.drone.flip('f')

    def telloFlip_b(self):
        return self.drone.flip('b')

    def telloCW(self):
        return self.drone.rotate_cw(self.degree)

    def telloCCW(self):
        return self.drone.rotate_ccw(self.degree)

    def telloMoveForward(self):
        return self.drone.move_forward(self.distance)

    def telloMoveBackward(self):
        return self.drone.move_backward(self.distance)

    def telloMoveLeft(self):
        return self.drone.move_left(self.distance)

    def telloMoveRight(self):
        return self.drone.move_right(self.distance)

    def telloUp(self):
        return self.drone.move_up(self.distance)

    def telloDown(self):
        return self.drone.move_down(self.distance)

    def on_close(self):
        print("[INFO] closing...")
        del self.gui
        del self.ai
        del self.pose
        del self.camera
        del self.drone
