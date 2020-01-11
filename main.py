import Problem
import sys, random, os

if __name__ == "__main__":
    models_path = "./Models/" + sys.argv[1] + "/"

    problem = Problem.Problem(models_path + random.choice(os.listdir(models_path)))