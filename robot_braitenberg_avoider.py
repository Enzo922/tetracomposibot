
from robot import * 

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "Avoider"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        wall = [sensors[i]*(sensor_view[i] == 1) + 1.0*(sensor_view[i] != 1) for i in range(8)]
        bot  = [sensors[i]*(sensor_view[i] == 2) + 1.0* (sensor_view[i] != 2) for i in range(8)]

        val = [min(wall[i], bot[i]) for i in range(8)]
        translation = val[sensor_front] * 0.7
        rotation = 0.5 * (val[sensor_front_left] -val[sensor_front_right])

        self.iteration = self.iteration + 1        
        return translation, rotation, False
