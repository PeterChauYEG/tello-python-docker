from robot import Robot
from fake_tello import FakeTello
from camera import Camera

if __name__ == "__main__":
    drone = FakeTello()
    camera = Camera()
    robot = Robot(drone, camera)

    robot.start()
