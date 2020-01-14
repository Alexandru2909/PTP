import Problem
import sys, random, os, datetime

if __name__ == "__main__":
    models_path = "./Models/" + sys.argv[1] + "/"

    problem = Problem.Problem(models_path + random.choice(os.listdir(models_path)))

    # a = problem.vehicles[0].getTimeWindows()
    # b = problem.vehicles[0].getTimeWindows()[0][1]

    
    # diff = datetime.datetime.combine(datetime.date.today(), b) - datetime.datetime.combine(datetime.date.today(), a)
    # print(a)
    # print(problem.distMatrix)

