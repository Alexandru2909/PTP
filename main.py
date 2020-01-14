import Problem
import sys, random, os, datetime

if __name__ == "__main__":
    models_path = "./Models/" + sys.argv[1] + "/"

    problem = Problem.Problem(models_path + random.choice(os.listdir(models_path)))

    problem.getRequests()
    for i in problem.orderReq():
        print(i.getReqTime())


    # print(problem.vehicles[0].history)