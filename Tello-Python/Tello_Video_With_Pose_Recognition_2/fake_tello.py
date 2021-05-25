class FakeTello:
    def __init__(self):
        pass

    def send_command(self, command):
        print('send command: %s' % command)

    def get_response(self):
        print('get response')
        return 'ok'

    def get_height(self):
        print('get height')
        return 10

    def land(self):
        print('land')

    def move_backward(self, distance):
        print('move_backward')

    def move_down(self, distance):
        print('move_down')

    def move_forward(self, distance):
        print('move_forward')

    def move_left(self, distance):
        print('move_left')

    def move_right(self, distance):
        print('move_right')

    def move_up(self, distance):
        print('move_up')

    def takeoff(self):
        print('takeoff')

    def flip(self, direction):
        print('flip %s' % direction)

    def rotate_cw(self, degree):
        print('rotate cw %s' % degree)

    def rotate_ccw(self, degree):
        print('rotate ccw %s' % degree)
