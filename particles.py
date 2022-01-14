import random
import math
import pygame
from easing_functions import *

# Particle
# [position [x, y],
# velocity [x, y],
# time remaining,
# size,
# opacity]

def normalize(vec):
    mag = math.sqrt(vec[0]**2 + vec[1]**2)
    if mag <= 0:
        return [0, 0]
    else:
        return [vec[0] / mag, vec[1] / mag]

def lerp(a, b, t):
    return a + t * (b - a)

def clamp(val, min_, max_):
    return min(max_, max(min_, val))

class particle_system():
    def __init__(self, spawner_position, spawner_radius, spawner_rate,
                        velocity, lifetime, size,
                        begin_color = (255, 255, 255), end_color = (255, 255, 255),
                        rnd_size = 0, rnd_lifetime = 0, rnd_velo = 0):
        print("Init particle system")
        self.particles = []

        self.spawner_pos = spawner_position
        self.spawner_rad = spawner_radius
        self.spawner_rate = spawner_rate
        self.spawner_spd = velocity
        self.spawner_lifetime = lifetime
        self.spawner_size = size

        self.random_size = rnd_size
        self.random_lifetime = rnd_lifetime
        self.random_velo = rnd_velo

        self.velo_ease_func = QuadEaseOut(start=1, end=0, duration = lifetime) 
        self.size_ease_func = QuadEaseInOut(start=1, end=0, duration = lifetime) 
        self.color_ease_func = QuadEaseInOut(start=0, end=1, duration = lifetime) 

        self.begin_color = begin_color
        self.end_color = end_color

        self.gravity = [0, -20]
    
    def step(self, dt):
        for i in range(self.spawner_rate):
            pos = self.spawner_pos;

            dir = normalize(
                [(random.random() * 2 - 1) * self.spawner_rad,
                (random.random() * 2 - 1) * self.spawner_rad]
            )

            pos = [pos[0] + dir[1], pos[1] + dir[1]]
            dir = [dir[0] * self.spawner_spd, dir[1] * self.spawner_spd]

            vel_rnd = normalize(
                [(random.random() * 2 - 1) * self.spawner_rad,
                (random.random() * 2 - 1) * self.spawner_rad]
            )
            rnd_velo_coefficient = (random.random() * 2 - 1) * self.random_velo
            vel_rnd = [vel_rnd[0] * rnd_velo_coefficient, vel_rnd[1] * rnd_velo_coefficient]

            dir = [dir[0] + vel_rnd[0], dir[1] + vel_rnd[1]]

            size = self.spawner_size + (random.random() * 2 - 1) * self.random_size
            life = self.spawner_lifetime + (random.random() * 2 - 1) * self.random_lifetime

            self.particles.append([pos, dir, life, size])

        for particle in self.particles:
            particle[1] = [particle[1][0] + self.gravity[0], particle[1][1] + self.gravity[1]]

            vel_coefficient = self.velo_ease_func(self.spawner_lifetime - particle[2])
            eval_velo = [particle[1][0] * vel_coefficient, particle[1][1] * vel_coefficient]

            particle[0][0] += eval_velo[0] * dt
            particle[0][1] += eval_velo[1] * dt
            particle[2] -= dt
            if particle[2] <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        index = 0
        for particle in self.particles:
            size = particle[3] * self.size_ease_func(self.spawner_lifetime - particle[2])
            color_blend = clamp(self.color_ease_func(clamp(self.spawner_lifetime - particle[2], 0, self.spawner_lifetime)), 0, 1)
            col = [
                max(min(int(lerp(self.begin_color[0], self.end_color[0], color_blend )), 255), 0),
                max(min(int(lerp(self.begin_color[1], self.end_color[1], color_blend )), 255), 0),
                max(min(int(lerp(self.begin_color[2], self.end_color[2], color_blend )), 255), 0)
            ]

            pygame.draw.circle(screen, color=col, center=[int(particle[0][0]), int(particle[0][1])], radius=size)
            index += 1