# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Bolea Alexandra
#  Prénom Nom No_étudiant/e : Tonati Enzo
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import *
import random

nb_robots = 0

class Robot_player(Robot):

    team_name = "BOLEA et TONATI"
    robot_id = -1
    memory = 0  # utilisé comme compteur de blocage

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name="Robot " + str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        front = 0
        front_left = 1
        front_right = 7

        # -------- Capteurs murs + ennemis --------
        wall = [sensors[i] if sensor_view[i] == 1 else 1.0 for i in range(8)]
        bot = [sensors[i] if sensor_view[i] == 2 and sensor_team[i] != self.team else 1.0 for i in range(8)]
        obstacles = [min(wall[i], bot[i]) for i in range(8)]

        # -------- Blocage (mur devant trop proche) --------
        if wall[front] < 0.2:
            self.memory += 1
        else:
            self.memory = 0

        if self.memory >= 5:
            # Stratégie de débloquage personnalisée par robot_id
            if self.robot_id == 0:
                rotation = 0.8  # tourner à gauche
            elif self.robot_id == 1:
                rotation = -0.8  # tourner à droite
            elif self.robot_id == 2:
                rotation = 1.0 if random.random() < 0.5 else -1.0  # pivot fort
            else:
                rotation = (random.random() - 0.5) * 2  # aléatoire complet
            return 0.0, rotation, False

        # -------- Évitement murs (commun) --------
        if min(obstacles[front], obstacles[front_left], obstacles[front_right]) < 0.85:
            translation = 0.7 * wall[front]
            rotation = 0.5 * (wall[front_left] - wall[front_right])
            if wall[front_left] < wall[front_right]:
                rotation -= 0.5
            else:
                rotation += 0.5
            return translation, rotation, False

        # -------- Évitement robots ennemis (commun) --------
        if bot[front] < 1.0:
            translation = (1.0 - bot[front]) * 0.7
            rotation = 0.5 * (bot[front_right] - bot[front_left])
            return translation, rotation, False

        # -------- Comportement par défaut personnalisé --------
        translation = 0.5

        if self.robot_id == 0:
            rotation = 0.15  # légère dérive gauche
        elif self.robot_id == 1:
            rotation = -0.15  # légère dérive droite
        elif self.robot_id == 2:
            rotation = 0.0  # priorité à aller tout droit
        else:
            rotation = (random.random() - 0.5) * 0.3  # dérive plus aléatoire

        return translation, rotation, False
