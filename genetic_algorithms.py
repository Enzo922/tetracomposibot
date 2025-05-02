from robot import *
import math
import random
import os

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "GeneticAlgo"
    robot_id = -1
    iteration = 0

    parent = []
    best_score = -float('inf')

    child = []
    child_score = 0
    eval_count = 0
    it_per_evaluation = 400
    replay_best = False

    x_0 = 0
    y_0 = 0
    theta_0 = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a", it_per_evaluation=400):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.it_per_evaluation = it_per_evaluation
        self.parent = [random.randint(-1, 1) for _ in range(8)]

        # Efface le fichier de log au tout premier robot et au début de l'exécution
        if self.robot_id == 0:
            open("results_log.txt", "w").close()

    def reset(self):
        self.theta = random.uniform(0, 2 * math.pi)
        self.x = self.x_0 + random.uniform(-0.1, 0.1)
        self.y = self.y_0 + random.uniform(-0.1, 0.1)
        super().reset()

    def mutate(self, parent):
        child = parent.copy()
        idx = random.randint(0, len(child) - 1)
        old_value = child[idx]
        new_value = random.choice([-1, 0, 1])
        while new_value == old_value:
            new_value = random.choice([-1, 0, 1])
        child[idx] = new_value
        return child

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        if not self.replay_best:
            if self.iteration % self.it_per_evaluation == 0:
                if self.iteration > 0:
                    score = self.log_sum_of_translation * (1 - abs(self.log_sum_of_rotation / self.it_per_evaluation))
                    self.child_score = score

                    # Enregistre la ligne dans results_log.txt
                    with open("results_log.txt", "a") as f:
                        f.write(f"genetic,{self.eval_count},{score},{self.best_score}\n")

                    if score > self.best_score:
                        self.best_score = score
                        self.parent = self.child.copy()

                    self.eval_count += 1

                    if self.eval_count >= 500:
                        self.replay_best = True
                        self.iteration = 0
                        return 0, 0, True

                self.child = self.mutate(self.parent)
                self.iteration += 1
                return 0, 0, True

        # Rejoue la meilleure stratégie en boucle
        if self.replay_best and self.iteration % 1000 == 0 and self.iteration > 0:
            self.iteration += 1
            return 0, 0, True

        p = self.parent if self.replay_best else self.child
        translation = math.tanh(p[0] + p[1]*sensors[sensor_front_left] + p[2]*sensors[sensor_front] + p[3]*sensors[sensor_front_right])
        rotation = math.tanh(p[4] + p[5]*sensors[sensor_front_left] + p[6]*sensors[sensor_front] + p[7]*sensors[sensor_front_right])

        self.iteration += 1
        return translation, rotation, False
