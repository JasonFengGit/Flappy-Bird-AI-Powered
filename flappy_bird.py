import pygame
from pygame import *
from pygame.locals import *
import math
import random
from sys import exit
import time
import neat

win_x = 400
win_y = 502 + 70

pygame.init()
window = display.set_mode((win_x, win_y))
display.set_caption("flappy bird")

distance = 0
print_count = 0
fly_count = 0
ground = 502
ground_lo = 0
background = image.load('images//background.png').convert()
speed = 2
jumping = False
jumping_time = 0
not_jumping_time = 0
not_jumping = False
SPECIAL = False
ground_count = 0
last_press, last_time, jump_time,last_g_time = 0, 0, 0, 0
d_time = 0

bird_images = {
    1: image.load('images//1.png').convert_alpha(),
    2: image.load('images//2.png').convert_alpha(),
    3: image.load('images//3.png').convert_alpha(),
    4: image.load('images//4.png').convert_alpha(),
    5: image.load('images//5.png').convert_alpha(),
    6: image.load('images//6.png').convert_alpha(),
    7: image.load('images//7.png').convert_alpha(),
    8: image.load('images//8.png').convert_alpha(),
    9: image.load('images//9.png').convert_alpha(),
    10: image.load('images//10.png').convert_alpha()
}
pipe_up = [image.load('images//pipe_up.png').convert_alpha() for i in range(10)]
pipe_down = [image.load('images//pipe_down.png').convert_alpha() for i in range(10)]
pause_image = image.load('images//pause.png').convert_alpha()
game_over_image = image.load('images//gameover.png').convert_alpha()
start_image = image.load('images//start.png').convert_alpha()
numbers = [image.load('images//numbers//%d.png' % i).convert_alpha() for i in range(10)]
ground_image = image.load('images//ground.png').convert()
alive_image = image.load('images//alive.png').convert()
gen_image = image.load('images//gen.png').convert()


def ground_move(speed):
    global ground_count, ground_lo
    ground_lo -= 0.1 * speed
    window.blit(ground_image, (ground_lo, 502))
    window.blit(ground_image, (ground_lo + 313, 502))
    window.blit(ground_image, (ground_lo + 626, 502))

    if ground_lo < -336:
        ground_lo = 0


class Bird:
    def __init__(self, genome, config):
        self.center = [130, 170]
        self.radius = 25
        self.decide = False
        self.face = 0
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome = genome

    def gravity(self):
        if self.center[1] + 25 <= ground:
            self.center[1] += 0.3

    def jump(self):
        global not_jumping
        self.center[1] -= 1
        if self.center[1] - 25 <= 0:
            self.center[1] = 25
        image_lo = [self.center[0] - 25, self.center[1] - 25]
        window.blit(bird_images[1], image_lo)
        not_jumping = False

    def display(self):
        global jumping_time, last_time, last_g_time, jumping, not_jumping, not_jumping_time

        if self.decide:
            if time.time() - last_time > 0.1 or jumping:
                self.jump()
                if not jumping:
                    jumping = True
                    jumping_time = time.time()
                if time.time() - jumping_time > 0.2:
                    jumping = False
                    last_time = time.time()

            else:
                
                if time.time() - last_g_time > 0.1:
                    self.gravity()
                    last_g_time = time.time()
                image_lo = [self.center[0] - 25, self.center[1] - 25]
                window.blit(bird_images[1], image_lo)
                

        else:
            if time.time() - last_g_time > 0.1:
                    self.gravity()
                    last_g_time = time.time()
            image_lo = [self.center[0] - 25, self.center[1] - 25]
            if not not_jumping:
                not_jumping_time = time.time()
                not_jumping = True
            window.blit(bird_images[1], image_lo)

    def get_info(self):
        global pipes, print_count
        index = 0
        for i in range(10):
            if pipes.x_list[i] + 90 > self.center[0]:
                index = i
                break
        self.face = index
        return [self.center[1], pipes.x_list[index] - 25, pipes.y_list[index]-25, pipes.y_list[index] - 170 + 25]

    def make_decision(self):
        global d_time
        s = self.net.activate(self.get_info())
        self.decide = False if s[0] < 0.5 else True


class PipeList:
    def __init__(self):
        self.x_list = [336 + i * 300 for i in range(5)]
        self.y_list = [random.randint(220, 300) if i % 2 == 0 else random.randint(400, 470) for i in range(5)]
        self.y_distance = 170

    def display(self):
        self.move()
        for i in range(5):
            window.blit(pipe_up[i], (self.x_list[i], self.y_list[i]))
            window.blit(pipe_down[i], (self.x_list[i], self.y_list[i] - self.y_distance - 369))

    def move(self):
        global score, score_list, SPECIAL
        for i in range(5):
            self.x_list[i] -= 0.1 * speed
            if self.x_list[i] + 85 < 130 and self.y_list[i] not in score_list:
                score += 1
                score_list.append(self.y_list[i])
            if self.x_list[i] < -100:
                score_list.remove(self.y_list[i])
                self.x_list.pop(i)
                self.y_list.pop(i)
                self.x_list.append(self.x_list[-1] + 300)
                self.y_list.append(random.randint(190, 330))


class Birds:
    def __init__(self, genomes, config):
        self.alive = 50
        self.l = [Bird(genome, config) for genome_id, genome in genomes]

    def display(self):
        global pipes
        for each in self.l:
            each.gravity()
            each.make_decision()
            each.display()
            each.genome.fitness = score * 300 + distance
            if crash(each, pipes) or each.center[1] + 25 > ground:
                self.alive = len(self.l)
                self.l.remove(each)


def in_pipe_range(bird, pipe):
    bird_x, bird_y = int(bird.center[0]), int(bird.center[1])
    x = int(pipe[0])
    y = int(pipe[1])
    return (bird_x + 20 in range(x, x+50) and (bird_y - 20 in range(0, y-170) or bird_y + 20 in range(y, ground))) or (bird_x + 30 in range(x, x+50) and (bird_y in range(0, y-170) or bird_y in range(y, ground))) or (bird_x in range(x, x+50) and (bird_y - 20 in range(0, y-170) or bird_y + 20 in range(y, ground)))



def crash(bird, pipes):
    pipe_a = (pipes.x_list[0], pipes.y_list[0])
    pipe_b = (pipes.x_list[1], pipes.y_list[1])
    if SPECIAL:
        return False
    return in_pipe_range(bird, pipe_a) or in_pipe_range(bird, pipe_b)


def display_number(number, x, y):
    number = str(number)
    x = x - 24
    for i in range(len(number) - 1, -1, -1):
        window.blit(numbers[int(number[i])], (x, y))
        x -= 25


def game(birds, pipes):
    global score, score_list, generation, distance
    for eve in pygame.event.get():
        if eve.type == QUIT:
            exit()
    score = 0
    distance = 0
    score_list = []
    distance = 0
    while True:
        for eve in pygame.event.get():
            if eve.type == QUIT:
                exit()
        window.blit(background, (0, 0))

        birds.display()
        pipes.display()
        ground_move(speed)
        display_number(birds.alive, 52,0)
        display_number(score, 400, 0)
        display_number(int(distance), 400, 530)
        distance += 0.1 * speed
        pygame.display.update()
        time.sleep(0.001)
        if birds.alive <= 0 or len(birds.l) == 0:
            time.sleep(0.5)
            return


def eval_genomes(genomes, config):
    global generation, pipes
    pipes = PipeList()
    birds = Birds(genomes, config)
    game(birds, pipes)
    generation += 1


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


generation = 0
pipes = PipeList()
run("config")
