import pygame
from math import pi
import Problem
import sys, random, os

clock = pygame.time.Clock()

def displayVehicle(screen, vehicleImg, x, y):
    screen.blit(vehicleImg, (x, y))

def draw(inst, places, patients):
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 255,   0)
    RED =   (255,   0,   0)

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    done = False


    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # F

        screen.fill(WHITE)
        # pygame.draw.arc(screen, BLACK,[210, 75, 150, 125], 0, pi/2, 2)
        # pygame.draw.arc(screen, BLACK, [-9.765289504081604 + 100, 0.09260531673304229 + 100, 50, 50], 0, 2*pi, 2)
        for place in places:
            if place.category == 0:
                pygame.draw.rect(screen, RED, [abs((place.lat) * 30 + 1000), abs((place.long) * 30 + 550), 15, 15], 2)
            elif place.category == 1:
                depot = place
                # print(abs((place.lat) * 30 + 1000), abs(place.long) * 30 + 550)
                pygame.draw.arc(screen, GREEN, [abs((place.lat) * 30 + 1000), abs((place.long) * 30 + 550), 25, 15], 0, 2*pi, 2)
            else:
                pygame.draw.arc(screen, BLACK, [abs((place.lat) * 30 + 1000), abs((place.long) * 30 + 550), 15, 15], 0, 2*pi, 2)

        vehicles = list()
        vehicleImg = pygame.image.load('./images/vehicle.png')
        # print(inst.vehicles)
        for vehicle in inst.vehicles:
            # print(len(inst.vehicles))
            # print(abs(vehicle.start.lat) * 30 + 1000, abs(vehicle.start.long) * 30 + 550, abs((depot.lat) * 30 + 1000), abs(depot.long) * 30 + 550)
            displayVehicle(screen, vehicleImg, abs(vehicle.start.lat) * 30 + 1000, abs(vehicle.start.long) * 30 + 550)

        # displayVehicle(screen, vehicleImg, 500, 500)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


models_path = "./Models/" + sys.argv[1] + "/"
problem = Problem.Problem(models_path + random.choice(os.listdir(models_path)))
draw(problem, problem.places, problem.patients)
