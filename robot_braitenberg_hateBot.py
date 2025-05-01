
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
        
        translation = (1.0 - wall[sensor_front]) * 0.7
        rotation = 0.5 * (wall[sensor_front_right] - wall[sensor_front_left])
        
        return translation, rotation, False

