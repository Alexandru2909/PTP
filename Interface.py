import pygame
from math import pi
import Problem
import sys, random, os
from datetime import timedelta
import time as t

clock = pygame.time.Clock()

def displayVehicle(screen, vehicleImg, x, y):
    screen.blit(vehicleImg, (x - 20 , y - 10))

def getPlaceByID(placeID, places):
    for p in places:
        if p.id == placeID:
            return p

def lineEquation(points):
    x1 = points[0][0]
    y1 = points[0][1]
    x2 = points[1][0]
    y2 = points[1][1]

    # print(y2)
    m = (y2 - y1)/(x2 - x1)
    b = y1 - m*x1
    return m, b

def draw(inst, vehicles, places, patients, maxWaitTime):
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 255,   0)
    RED =   (255,   0,   0)

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    done = False

    world_time = timedelta(hours=7, minutes=0)
    placesToBe = list()
    firtstIter = True
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # F

        screen.fill(WHITE)
        # pygame.draw.arc(screen, BLACK,[210, 75, 150, 125], 0, pi/2, 2)
        # pygame.draw.arc(screen, BLACK, [-9.765289504081604 + 100, 0.09260531673304229 + 100, 50, 50], 0, 2*pi, 2)
        for place in places:
            if place.category == 0:
                if firtstIter == True:
                    pygame.draw.rect(screen, RED, [abs(place.lat) * 30 + 1000, abs((place.long) * 30 + 550), 15, 15], 2)
                    place.lat = abs(place.lat) * 30 + 1000
                    place.long = abs(place.long) * 30 + 550
                else:
                    pygame.draw.rect(screen, RED, [place.lat, place.long, 15, 15], 2)
            elif place.category == 1:
                if firtstIter == True:
                    pygame.draw.arc(screen, GREEN, [abs(place.lat) * 30 + 1000, abs((place.long) * 30 + 550), 25, 15], 0, 2*pi, 2)
                    place.lat = abs(place.lat) * 30 + 1000
                    place.long = abs(place.long) * 30 + 550
                else:
                    pygame.draw.arc(screen, GREEN, [place.lat, place.long, 25, 15], 0, 2*pi, 2)
            else:
                if firtstIter == True:
                    pygame.draw.arc(screen, BLACK, [abs(place.lat) * 30 + 1000, abs((place.long) * 30 + 550), 15, 15], 0, 2*pi, 2)
                    place.lat = abs(place.lat) * 30 + 1000
                    place.long = abs(place.long) * 30 + 550
                else:
                    pygame.draw.arc(screen, BLACK, [place.lat, place.long, 15, 15], 0, 2*pi, 2)
            print(place.lat, place.long)
            

        vehicleImg = pygame.image.load('./images/vehicle.png')
        for vehicle in vehicles:
            if vehicle[1] == True:
                vehicle[0].history = vehicle[0].history[1:]
                startPlace = getPlaceByID(vehicle[0].start, places)
                displayVehicle(screen, vehicleImg, abs(startPlace.lat) * 30 + 1000, abs(startPlace.long) * 30 + 550)
                vehicle[1] = False
                nextPlace = getPlaceByID(vehicle[0].history[0].place, places)
                placesToBe.append((abs(startPlace.lat) * 30 + 1000, abs(startPlace.long) * 30 + 550))
                placesToBe.append((abs(nextPlace.lat) * 30 + 1000, abs(nextPlace.long) * 30 + 550))
            else:
                if vehicle[0].history[0].time == world_time:
                    vehicle[0].history = vehicle[0].history[1:]
                    vehicleIndex = vehicles.index(vehicle)
                    displayVehicle(screen, vehicleImg, placesToBe[vehicleIndex][1][0], placesToBe[vehicleIndex][1][1])
                    nextPlace = getPlaceByID(vehicle.history[0].place, places)
                    placesToBe[vehicleIndex][0] = placesToBe[vehicleIndex][1]
                    placesToBe[vehicleIndex][1] = ((abs(nextPlace.lat) * 30 + 1000, abs(nextPlace.long) * 30 + 550))
                else:

                    a,b = lineEquation(placesToBe)
                    deparure_time = vehicle[0].history[0].time
                    x = (abs(placesToBe[0][0] - placesToBe[1][0])/((world_time.seconds/60) - (vehicle[0].history[0].time.seconds/60))) * (world_time.seconds/60) - (deparure_time.seconds/60)
                    y = a*x + b
                    displayVehicle(screen, vehicleImg, x, y)


        # displayVehicle(screen, vehicleImg, 500, 500)
        pygame.display.update()
        clock.tick(60)

        print(world_time)
        t.sleep(1)
        world_time += timedelta(minutes=1)
        firtstIter = False
    pygame.quit()


models_path = "./Models/" + sys.argv[1] + "/"
# problem = Problem.Problem(models_path + random.choice(os.listdir(models_path)))
problem = Problem.Problem("./Models/easy/PTP-RAND-1_4_2_16.json")

inst = problem.search(0)
# print(inst)

new_vehicles = list()
for vehicle in inst.vehicles:
    new_vehicles.append([vehicle, True])
# print(new_vehicles[0][0].history[0].place)
draw(problem, new_vehicles, problem.places, problem.patients, problem.maxWaitTime)
