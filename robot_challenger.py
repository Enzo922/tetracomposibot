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
        front = 0
        front_left = 1
        front_right = 7
        #eviter les murs
        wall = [sensors[i] if sensor_view[i] == 1 else 1.0 for i in range(8)]
        if min(wall[front], wall[front_left], wall[front_right]) < 0.9:
            translation = 0.7 * wall[front]
            rotation = 0.5 * (wall[front_left] - wall[front_right])
            return translation, rotation, False

        # eviter les autres robots de son equipe
        bot = [sensors[i] if sensor_view[i] == 2 and sensor_team[i] != self.team else 1.0 for i in range(8)]
        if bot[front] < 1.0:
            translation = (1.0 - bot[front]) * 0.7
            rotation = 0.5 * (bot[front_right] - bot[front_left])
            return translation, rotation, False

        # tout droit
        translation = 0.5
        rotation = (random.random() - 0.5) * 0.1
        return translation, rotation, False
