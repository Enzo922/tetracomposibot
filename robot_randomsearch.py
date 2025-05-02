from robot import *
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "RandomSearch"
    robot_id = -1
    iteration = 0

    current_score = 0
    best_score = -float('inf')
    best_param = []

    param = []
    trial = 0
    nb_evaluations = 500
    it_per_evaluation = 400
    replay_best = False

    x_0 = 0
    y_0 = 0
    theta_0 = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a", evaluations=500, it_per_evaluation=400):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.nb_evaluations = evaluations
        self.it_per_evaluation = it_per_evaluation
        self.param = [random.randint(-1, 1) for _ in range(8)]

    def reset(self):
        super().reset()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # Phase d'optimisation
        if not self.replay_best:
            if self.iteration % self.it_per_evaluation == 0:
                if self.iteration > 0:
                    score = self.log_sum_of_translation * (1 - abs(self.log_sum_of_rotation / self.it_per_evaluation))
                    with open("results_log.txt", "a") as f:
                        f.write(f"randomsearch,{self.trial},{self.trial_score},{self.best_score}\n")



                    if score > self.best_score:
                        self.best_score = score
                        self.best_param = self.param.copy()
                        print(" New best strategy!")

                self.trial += 1

                if self.trial >= self.nb_evaluations:
                    print("\n Switching to replay mode. Best strategy found:")
                    print("  Best Score :", self.best_score)
                    print("  Best Params:", self.best_param)
                    self.replay_best = True
                    self.iteration = 0
                    return 0, 0, True  # Reset for replay
                else:
                    self.param = [random.randint(-1, 1) for _ in range(8)]
                    self.iteration += 1
                    return 0, 0, True  # Reset for new trial

        # Phase de "replay" du meilleur comportement
        if self.replay_best and self.iteration % 1000 == 0 and self.iteration > 0:
            self.iteration += 1
            return 0, 0, True  # Reset toutes les 1000 itérations

        # Calcul des commandes via Perceptron
        p = self.best_param if self.replay_best else self.param

        translation = math.tanh(p[0] + p[1]*sensors[sensor_front_left] + p[2]*sensors[sensor_front] + p[3]*sensors[sensor_front_right])
        rotation = math.tanh(p[4] + p[5]*sensors[sensor_front_left] + p[6]*sensors[sensor_front] + p[7]*sensors[sensor_front_right])

        self.iteration += 1
        return translation, rotation, False
