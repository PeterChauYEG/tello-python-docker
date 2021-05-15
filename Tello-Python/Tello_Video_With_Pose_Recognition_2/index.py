from robot import Robot
from tello import Tello
from camera import Camera

if __name__ == "__main__":
    drone = Tello('', 8889)
    robot = Robot(drone, drone)  # robot

    # camera = Camera()
    # robot = Robot(drone, camera) # Mac

    robot.start()
