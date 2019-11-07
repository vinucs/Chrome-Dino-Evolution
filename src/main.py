import GeneticAlgorithm
import Player
import Sprite
import time
import random
import pygame

def createDino():
    dinosaur = Sprite.Dinosaur(dino_posx, dino_posy, 0, jump_aceleration, down_aceleration)
    dinosaur.setSprites(dinosaur_walk_sprite, dinosaur_crouch_sprite)
    dinosaur.setDinoHitBox(dino_lenght_walk, dino_height_walk, dino_lenght_crouch, dino_height_crouch)
    return dinosaur

def createCactus(posx):
    cactus = Sprite.Cactus(posx, cactus_posy, destroy_obj_dist)
    cactus.setSprites(cactus_sprite)
    cactus.setHitBox(cactus_lenght, cactus_height)
    return cactus

def createBird(posx):
    bird = Sprite.Bird(posx, bird_posy[1], destroy_obj_dist)
    bird.setSprites(bird_sprite, time.time())
    bird.setHitBox(bird_lenght, bird_height)
    return bird

def createGround(posx):
    ground = Sprite.Ground(posx, ground_posy, destroy_grnd_dist)
    ground.setSprites(ground_sprite)
    return ground

def createCloud(posx):
    cloud = Sprite.Cloud(posx, cloud_posy[random.randint(0,1)], destroy_obj_dist)
    cloud.setSprites(cloud_sprite)
    return cloud

def drawBackground():
    ground = []
    pos = 0
    for i in range(3):
        ground.append(createGround(pos))
        pos += ground_lenght
    for x in ground:
        display.blit(x.getSprite(), x.getPosition())
    cloud = []
    pos = display_width*0.5
    for i in range(4):
        cloud.append(createCloud(pos))
        pos += 300
    for x in cloud:
        display.blit(x.getSprite(), x.getPosition())
    return ground, cloud

def verifySpritesOnScreen():
    i = 0
    while(i < len(obstacle_list)):
        if obstacle_list[i].posx < obstacle_list[i].max_dist:
            obstacle_list.pop(i)
        else:
            i += 1
    i = 0
    while(i < len(cloud_list)):
        if cloud_list[i].posx < cloud_list[i].max_dist:
            cloud_list.pop(i)
        else:
            i += 1
    if len(cloud_list) == 0:
        cloud_list.append(createCloud(display_width*0.5))
    elif len(cloud_list) < 4:
        cloud_list.append(createCloud(cloud_list[-1].posx + 300))
    i = 0
    while(i < len(ground_list)):
        if ground_list[i].posx < ground_list[i].max_dist:
            ground_list.pop(i)
        else:
            i += 1
    if len(ground_list) == 0:
        ground_list.append(createGround(ground_lenght))
    elif len(ground_list) < 3:
        ground_list.append(createGround(ground_list[-1].posx + ground_lenght))

def createObstacle(respawn_obj_dist):
    if len(obstacle_list) > 0:
        if display_width - obstacle_list[-1].posx > respawn_obj_dist:
            if random.uniform(0,1) < respawn_obj_chance:
                which_type = random.uniform(0,1)
                if which_type < 0.7:                     
                    obstacle_list.append(createCactus(display_width))
                elif which_type < 1:
                    obstacle_list.append(createBird(display_width))
                # elif which_type <= 1:
                #     obstacle_list.append(createCactus(display_width))
                #     obstacle_list.append(createCactus(display_width + 30))
                #     obstacle_list.append(createCactus(display_width + 60))
                respawn_obj_dist = 300
            else:
                respawn_obj_dist += 100
    else:
        obstacle_list.append(createCactus(display_width))
    return respawn_obj_dist

def moveScreen():
    for x in range(len(obstacle_list)):
        obstacle_list[x].move(game_speed, 0)
        obstacle_list[x].updateHitBox()
    for x in range(len(cloud_list)):
        cloud_list[x].move(game_speed, 0)
    for x in range(len(ground_list)):
        ground_list[x].move(game_speed, 0)

def dinoMovement(dinosaur_list):
    if dinosaur_list.dinosaur.grounded == False:
        dinosaur_list.dinosaur.posy -= dinosaur_list.dinosaur.aceleration* (1.0/tickrate)
        dinosaur_list.dinosaur.aceleration -= gravity
        if dinosaur_list.dinosaur.posy > dino_posy:
            dinosaur_list.dinosaur.isGrounded(dino_posy)
        dinosaur_list.dinosaur.updateDinoHitbox()

def spriteUpdate(dinosaur):
    if (time.time() - dinosaur.sprite_time) > update_sprite_frequency:
        dinosaur.dinosaur.updateSprite()
        return time.time()
    return dinosaur.sprite_time

def spriteBirdUpdate():
    for x in range(len(obstacle_list)):
        if type(obstacle_list[x]) == Sprite.Bird:
            if (time.time() - obstacle_list[x].sprite_time) > bird_sprite_frequency:
                obstacle_list[x].updateSprite()
                obstacle_list[x].sprite_time = time.time()

def verifyHitBox(dinosaur):
    for i in obstacle_list:
        # subindo
        if dinosaur.dinosaur.hitbox[1] <= i.hitbox[3] and dinosaur.dinosaur.hitbox[3] >= i.hitbox[1]:
            if dinosaur.dinosaur.hitbox[2] >= i.hitbox[0] and dinosaur.dinosaur.hitbox[0] <= i.hitbox[2]:
                return True
        # descendo
        if dinosaur.dinosaur.hitbox[1] >= i.hitbox[3] and dinosaur.dinosaur.hitbox[3] <= i.hitbox[1]:
            if dinosaur.dinosaur.hitbox[2] >= i.hitbox[0] and dinosaur.dinosaur.hitbox[0] <= i.hitbox[2]:
                return True
    return False

def calculateFitness(fitness, game_speed):
    fitness -= game_speed*(1.0/tickrate)
    return fitness

def increaseDifficulty(game_speed, fitness):
    if fitness % increase_difficulty_dist <= 0.09:
        game_speed -= 100
        if game_speed < max_game_speed:
            game_speed = max_game_speed
    return game_speed

def getClosestObstacle(dinosaur):
    for x in obstacle_list:
        if x.hitbox[0] - dinosaur.dinosaur.hitbox[2] >= 0:
            return obstacle_list.index(x)
    return 0

def drawScreen(dinosaur):
    for x in obstacle_list:
        display.blit(x.getSprite(), x.getPosition())
    for x in cloud_list:
        display.blit(x.getSprite(), x.getPosition())
    for x in ground_list:
        display.blit(x.getSprite(), x.getPosition())
    for x in dinosaur:
        if x.game_over == False:
            display.blit(x.dinosaur.getSprite(), x.dinosaur.getPosition())

def drawText(fitness, game_speed, players_alive, generation, best_fitness):
    fit_text = text_font.render("Fitness: " + str(int(fitness)), True, dimgray)
    display.blit(fit_text, fit_text_pos)
    speed_text = text_font.render("Game speed: " + str(abs(game_speed)), True, dimgray)
    display.blit(speed_text, speed_text_pos)
    dino_alive_text = text_font.render("Players alive: " + str(players_alive), True, dimgray)
    display.blit(dino_alive_text, dino_alive_pos)
    gen_text = text_font.render("Generation: " + str(generation), True, dimgray)
    display.blit(gen_text, gen_text_pos)
    bfit_text = text_font.render("Best fitness: " + str(best_fitness), True, dimgray)
    display.blit(bfit_text, bfit_text_pos)

def drawHitBox(dinosaur_list):
    for x in dinosaur_list:
        if x.game_over == False:
            pygame.draw.rect(display, red, (x.dinosaur.hitbox[0], x.dinosaur.hitbox[1], x.dinosaur.hitbox_lenght, x.dinosaur.hitbox_height))
    for x in obstacle_list:
        pygame.draw.rect(display, red, (x.hitbox[0], x.hitbox[1], x.hitbox_lenght, x.hitbox_height))


### Set pygame
pygame.init()
display_width = 1280
display_height = 720
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
dimgray = (105,105,105)
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Chrome Dino with Machine Learning')
display.fill(white)
clock = pygame.time.Clock()
tickrate = 60
update_sprite_frequency = 1.0/15
bird_sprite_frequency = 1.0/5

### Set text on screen
text_font = pygame.font.Font('freesansbold.ttf', 20)
dino_alive_pos = (display_width *0.8, display_height *0.04)
fit_text_pos = (display_width *0.8, display_height *0.08)
speed_text_pos = (display_width *0.8, display_height *0.12)
gen_text_pos = (display_width *0.4, display_height *0.04)
bfit_text_pos = (display_width *0.4, display_height *0.08)

### Set game parameters
gravity = 18
jump_aceleration = 380
down_aceleration = -300
dino_posx = display_width *0.1
dino_posy = display_height *0.82
dino_height_walk = 42
dino_lenght_walk = 42
dino_height_crouch = 27
dino_lenght_crouch = 55
cactus_posy = display_height *0.82
cactus_height = 45
cactus_lenght = 26
bird_posy = (display_height *0.83, display_height *0.78)
bird_height = 30
bird_lenght = 43
cloud_posy = (display_height *0.65, display_height *0.7)
ground_posy = display_height *0.77
ground_lenght = 1195
respawn_obj_chance = 0.5
respawn_obj_dist = 300
destroy_obj_dist = -50
destroy_grnd_dist = -ground_lenght
game_speed = -5
increase_difficulty_dist = 50
max_game_speed = -10

### Set sprites
dinosaur_walk_sprite = [pygame.image.load('image/sprites/dinosaur/dino_walking_1.png'), pygame.image.load('image/sprites/dinosaur/dino_walking_2.png'), 
    pygame.image.load('image/sprites/dinosaur/dino_walking_3.png')]
dinosaur_crouch_sprite = [pygame.image.load('image/sprites/dinosaur/dino_crouch_1.png'), pygame.image.load('image/sprites/dinosaur/dino_crouch_2.png')]
bird_sprite = [pygame.image.load('image/sprites/bird/bird_1.png'), pygame.image.load('image/sprites/bird/bird_2.png')]
cactus_sprite = pygame.image.load('image/sprites/cactus/cactus_1.png')
ground_sprite = pygame.image.load('image/background/ground.png')
cloud_sprite = pygame.image.load('image/background/cloud.png')

### Set Neural Evolution parameters
num_population = 100
mutation_factor = 0.5
crossover_rate = 0.8
input_number = 4 # distancia, altura, velocidade, bias
hidden_number = 6
output_number = 3 # pular, agachar, nada
max_weight_value = 100
min_weight_value = -100
weights_number = (input_number*hidden_number)+(hidden_number*output_number)

### Initialize Neural Evolution
dino_evolution = GeneticAlgorithm.GeneticAlgorithm(num_population, mutation_factor, crossover_rate, max_weight_value, min_weight_value, weights_number)
dino_evolution.createPopulation()
generation = 1
best_fitness = 0
while generation <= 50:
    dinosaur_players = []
    population_over = [False]*num_population
    for x in range(num_population):
        dinosaur_players.append(Player.Player(createDino(), x, time.time()))
        dinosaur_players[x].createNeuralNetwork(input_number, hidden_number, output_number)
        dinosaur_players[x].setNeuralNetworkWeights(dino_evolution.getPopulation()[x][:-1])
        dinosaur_players[x].setBias(dino_evolution.getPopulation()[x][-1])
        dinosaur_players[x].setPlayerFitness(0)

    ### Draw screen
    ground_list, cloud_list = drawBackground()
    obstacle_list = []

    ### Program loop
    close_program = False
    fitness = 0
    game_speed = -5
    random.seed(11)
    while not close_program:
        clock.tick(tickrate)

        # Check Keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_program = True
        #     if event.type == pygame.KEYUP:
        #         if event.key == pygame.K_DOWN:
        #             dinosaur.isWalking()
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_DOWN]:
        #     dinosaur.isCrouch()
        # if keys[pygame.K_UP]:
        #     dinosaur.isJumping()

        # Update Game
        verifySpritesOnScreen()
        moveScreen()
        spriteBirdUpdate()
        respawn_obj_dist = createObstacle(respawn_obj_dist)
        fitness = calculateFitness(fitness, game_speed)
        game_speed = increaseDifficulty(game_speed, fitness)
        closest = getClosestObstacle(dinosaur_players[0])
        input_values = [(obstacle_list[closest].hitbox[0] - dino_posx), abs(obstacle_list[closest].hitbox[1] - dino_posy), abs(game_speed)]
        for i in range(len(dinosaur_players)):
            dinosaur_players[i].updateInputValues(input_values)
            dinosaur_players[i].makeDecision()
            dinosaur_players[i].setPlayerFitness(fitness)
            dinoMovement(dinosaur_players[i])
            dinosaur_players[i].sprite_time = spriteUpdate(dinosaur_players[i])
            if population_over[i] == False:
                population_over[i] = verifyHitBox(dinosaur_players[i])
                if population_over[i] == True:
                    dinosaur_players[i].gameOver()

        # Players alive
        num_pop_over = 0
        for i in population_over:
            if i == True:
                num_pop_over += 1

        # Update Screen
        display.fill(white)
        drawText(fitness, game_speed, num_population - num_pop_over, generation, best_fitness)
        drawHitBox(dinosaur_players)
        drawScreen(dinosaur_players)
        pygame.display.flip()

        if num_pop_over == len(population_over):
            break
    
    ground_list.clear()
    cloud_list.clear()
    obstacle_list.clear()
    if close_program == True:
        break

    # Mutation and Crossover Phase
    genalg_text = text_font.render("Selecting the best childrens", True, dimgray)
    display.blit(genalg_text, (display_width *0.1, display_height*0.05))
    pygame.display.flip()
    time.sleep(0.5)
    population_fitness = []
    for i in range(num_population):
        population_fitness.append(int(dinosaur_players[i].getPlayerFitness()))
    dino_evolution.setFitness(population_fitness)
    dino_evolution.improveIndividuals()

    # Selection Phase
    pygame.display.flip()
    population_over = [False]*num_population
    dinosaur_players.clear()
    for x in range(num_population):
        dinosaur_players.append(Player.Player(createDino(), x, time.time()))
        dinosaur_players[x].createNeuralNetwork(input_number, hidden_number, output_number)
        dinosaur_players[x].setNeuralNetworkWeights(dino_evolution.getChildrens()[x][:-1])
        dinosaur_players[x].setBias(dino_evolution.getPopulation()[x][-1])
        dinosaur_players[x].setPlayerFitness(0)
    ground_list, cloud_list = drawBackground()
    obstacle_list = []
    game_over = False
    fitness = 0
    game_speed = -5
    random.seed(11)
    while not close_program:

        # Check Keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_program = True
        
        # Update Game
        verifySpritesOnScreen()
        moveScreen()
        respawn_obj_dist = createObstacle(respawn_obj_dist)
        fitness = calculateFitness(fitness, game_speed)
        game_speed = increaseDifficulty(game_speed, fitness)
        closest = getClosestObstacle(dinosaur_players[0])
        input_values = [obstacle_list[closest].hitbox[0], (obstacle_list[closest].hitbox[3] - dino_posy), game_speed]
        for i in range(len(dinosaur_players)):
            dinosaur_players[i].updateInputValues(input_values)
            dinosaur_players[i].makeDecision()
            dinosaur_players[i].setPlayerFitness(fitness)
            dinoMovement(dinosaur_players[i])
            if population_over[i] == False:
                population_over[i] = verifyHitBox(dinosaur_players[i])
                if population_over[i] == True:
                    dinosaur_players[i].gameOver()

        # Childrens alive
        num_pop_over = 0
        for i in population_over:
            if i == True:
                num_pop_over += 1
        if num_pop_over == len(population_over):
            break

    childrens_fitness = []
    for i in range(num_population):
        childrens_fitness.append(int(dinosaur_players[i].getPlayerFitness()))
    dino_evolution.setChildrensFitness(childrens_fitness)
    print(childrens_fitness)
    dino_evolution.selection()

    generation += 1
    if max(population_fitness) > best_fitness:
        best_fitness = max(population_fitness)

print(best_fitness)
pygame.quit()
quit()