
from robot import * 

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "Dumb"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        wall = [sensors[i] * (sensor_view[i] == 1) + 1.0 * (sensor_view[i] != 1) for i in range(8)]
        avoid_wall = wall[sensor_front] * 0.7
        rotate_wall = 0.5 * (wall[sensor_front_left] - wall[sensor_front_right])

        bot = [sensors[i] * (sensor_view[i] == 2) + 1.0 * (sensor_view[i] != 2) for i in range(8)]
        towards_robot = (1.0 - bot[sensor_front]) * 0.7
        rotate_robot = 0.5 * (bot[sensor_front_right] - bot[sensor_front_left])

        go_straight = 0.5  
        
        translation = 0
        rotation = 0

        #1ere priorite eviter les murs
        if wall[sensor_front] < 1.0:
            translation = avoid_wall
            rotation = rotate_wall
        # 2eme priorite love robot
        elif bot[sensor_front] < 1.0:
            translation = towards_robot
            rotation = rotate_robot
        #moins prioritaire go straight
        else:
            translation = go_straight
            rotation = 0

        return translation, rotation, False
