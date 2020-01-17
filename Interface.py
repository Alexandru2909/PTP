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
    print("Points: ", points)
    x1 = points[0][0]
    y1 = points[0][1]
    x2 = points[1][0]
    y2 = points[1][1]

    # print(y2)
    if x2 - x1 == 0:
        return (1,1)
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

    for place in places:
        place.lat = abs(place.lat) * 50 + 700
        place.long = abs(place.long) * 50 + 300
               
    font = pygame.font.Font('freesansbold.ttf', 20) 
    text = font.render("str(world_time)", True, GREEN, BLUE) 
    textRect = text.get_rect()
    textRect.center = (100, 100) 
    while not done:
        screen.fill(WHITE)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done=True # F

        s = world_time.seconds
        hours = s //3600
        s = s - (hours * 3600)
        minutes = s // 60
        seconds = s - (minutes * 60)
        text_surface = font.render('{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds)), True, (0, 0, 0))
        screen.blit(text_surface, dest=(250, 150))

        # pygame.draw.arc(screen, BLACK,[210, 75, 150, 125], 0, pi/2, 2)
        # pygame.draw.arc(screen, BLACK, [-9.765289504081604 + 100, 0.09260531673304229 + 100, 50, 50], 0, 2*pi, 2)
        for place in places:
            if place.category == 0:
                pygame.draw.rect(screen, RED, [place.lat, place.long, 15, 15], 2)
            elif place.category == 1:
                pygame.draw.arc(screen, GREEN, [place.lat, place.long, 25, 15], 0, 2*pi, 2)
            else:
                pygame.draw.arc(screen, BLACK, [place.lat, place.long, 15, 15], 0, 2*pi, 2)
            

        vehicleImg = pygame.image.load('./images/vehicle.png')
        for vehicle in vehicles:
            if vehicle[1] == True:
                print("Prima data")
                startPlace = getPlaceByID(vehicle[0].start, places)
                displayVehicle(screen, vehicleImg, startPlace.lat, startPlace.long)
                # print(abs(startPlace.lat) * 50 + 700, abs(startPlace.long) * 50 + 300)
                vehicle[1] = False
                nextPlace = getPlaceByID(vehicle[0].history[1].place, places)
                placesToBe.append([(startPlace.lat, startPlace.long), (nextPlace.lat, nextPlace.long)])
            else:
                if vehicle[0].history[0].time == world_time:
                    print("La activity")
                    vehicle[0].history = vehicle[0].history[1:]
                    vehicleIndex = vehicles.index(vehicle)
                    displayVehicle(screen, vehicleImg, placesToBe[vehicleIndex][1][0], placesToBe[vehicleIndex][1][1])
                    print("Old: ", placesToBe[vehicleIndex])
                    nextPlace = getPlaceByID(vehicle[0].history[0].place, places)
                    placesToBe[vehicleIndex][0] = placesToBe[vehicleIndex][1]
                    placesToBe[vehicleIndex][1] = ((nextPlace.lat, nextPlace.long))
                    print("New: ", placesToBe[0])
                elif vehicle[0].history[0].time < world_time:
                    print("Pe parcurs")
                    vehicleIndex = vehicles.index(vehicle)
                    a,b = lineEquation(placesToBe[0])
                    deparure_time = vehicle[0].history[0].time
                    x = (abs(placesToBe[vehicleIndex][0][0] - placesToBe[vehicleIndex][1][0])/((vehicle[0].history[1].time.seconds/60) - (vehicle[0].history[0].time.seconds/60))) * (world_time.seconds/60) - (deparure_time.seconds/60)
                    y = a*x + b
                    displayVehicle(screen, vehicleImg, x, y)
                else:
                    vehicleIndex = vehicles.index(vehicle)
                    displayVehicle(screen, vehicleImg, placesToBe[vehicleIndex][0][0], placesToBe[vehicleIndex][0][1])


        # displayVehicle(screen, vehicleImg, 500, 500)
        pygame.display.update()
        clock.tick(60)

        # print(world_time)
        t.sleep(0.1)
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
