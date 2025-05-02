# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Bolea Alexandra
#  Prénom Nom No_étudiant/e : Tonati Enzo
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 

nb_robots = 0

class Robot_player(Robot):

    team_name = "Challenger"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        sensor_front = 0
        sensor_front_left = 1
        sensor_left = 2
        sensor_rear_left = 3
        sensor_rear = 4
        sensor_rear_right = 5
        sensor_right = 6
        sensor_front_right = 7
    
        wall = [sensors[i] if sensor_view[i] == 1 else 1.0 for i in range(8)]
        bot = [sensors[i] if sensor_view[i] == 2 and sensor_team[i] != self.team else 1.0 for i in range(8)]

        # murs + bot
        obstacles = [min(wall[i], bot[i]) for i in range(8)]

        #calcul la meilleure reorientation
        free_space = [1.0 - obstacles[i] for i in range(8)]
        max_free_space = max(free_space)
        best_direction = free_space.index(max_free_space)
        
        translation = 0.5 
        if max_free_space < 0.5:
            translation *= 0.5
            
        if best_direction == sensor_front:
            rotation = 0.0
        elif best_direction == sensor_front_left:
            rotation = 0.5
        elif best_direction == sensor_left:
            rotation = 0.7
        elif best_direction == sensor_rear_left:
            rotation = 0.8
        elif best_direction == sensor_rear:
            rotation = 1.0
        elif best_direction == sensor_rear_right:
            rotation = -0.8
        elif best_direction == sensor_right:
            rotation = -0.7
        elif best_direction == sensor_front_right:
            rotation = -0.5

        return translation, rotation, False
