import pygame
from random import randint, uniform
from math import sin, cos, radians
from enum import Enum

from math_util import Vector2, normalize, sqr_magnitude, lerp
from GUI import Text, FontPaths, Anchors
import game_over_screen
import save

score = 0

# PLAYER
player_position = Vector2(0, -500) # The current position of the player
base_player_speed = 1000 # The base movement speed of the player
player_velocity = Vector2() # The current velocity of the player

# Player states
class PlayerState(Enum):
    IDLE = 0
    MOVING = 1
    DEAD = 2
player_state = PlayerState.IDLE

# Particles for point collection format:
# [position, velocity, size]
collection_particles = []

# POINTS
class Point:
    def __init__(self, position, orbit_layers):
        # 'Orbit layers' are lists with the following format:
        # [(count, spread, distance, size, base_speed, sine_speed_amp, sine_speed_freq, sine_distance_amp, sine_distance_freq)]
        self.orbit_layers = orbit_layers

        # Initalize empty list for layers of obstacles
        self.obstacle_layers = []

        # Create obstacles for each orbit layer
        for orbit_layer in orbit_layers:

            # Initialize empty obstacle layer list
            obstacle_layer = []

            obstacle_count = orbit_layer[0]
            radians_spread = radians(orbit_layer[1])
            obstacle_size = orbit_layer[3]

            # Create individual obstacles
            for i in range(0, obstacle_count):
                angle = radians_spread * i
                obstacle_layer.append(Vector2(cos(angle), sin(angle)))
            
            # Add individual obstacle layer to layer list
            self.obstacle_layers.append(obstacle_layer)

        self.position = position

        # Set cleared to false
        self.cleared = False

        # Start with elapsed time at 0
        self.elapsed_time = 0

    # Returns the closest sqr distance to the given point
    def get_sqr_distance(self, point):
        min_distance = float("inf")
        for obstacle_layer in self.obstacle_layers:
            for obstacle in obstacle_layer:
                distance = sqr_magnitude(obstacle - point)
                if distance < min_distance:
                    min_distance = distance
        return min_distance

    def update(self, delta_time):
        global player_position

        if not self.cleared:
            # Iterate through each obstacle layer
            for i in range(0, len(self.obstacle_layers)):

                # Get current orbit layer
                orbit_layer = self.orbit_layers[i]

                # Get layer attributes from tuple
                radians_spread = radians(orbit_layer[1])
                base_distance = orbit_layer[2]
                base_speed = orbit_layer[4]

                sine_speed_amp = orbit_layer[5]
                sine_speed_freq = radians(orbit_layer[6])

                sine_distance_amp = orbit_layer[7]
                sine_distance_freq = radians(orbit_layer[8])

                for j in range(0, len(self.obstacle_layers[i])):
                    angle = (radians_spread * j) + (self.elapsed_time * base_speed) + (sin(self.elapsed_time * sine_speed_freq) * sine_speed_amp)
                    orbit_distance = ((i + 1) * base_distance + sin(angle + self.elapsed_time * sine_distance_freq) * sine_distance_amp)
                    self.obstacle_layers[i][j] = self.position + Vector2(cos(angle), sin(angle)) * orbit_distance

        # Update to elapsed time
        self.elapsed_time += delta_time

    def draw(self, surface, camera_position):

        # Get screen position and draw base point circle
        screen_position = self.position - camera_position
        pygame.draw.circle(
            window,
            color=(255, 255, 255),
            center=[screen_position.x, screen_position.y],
            radius=point_radius,
            width=point_width
        )

        if not self.cleared:
            # Iterate through each obstacle layer
            for i in range(0, len(self.obstacle_layers)):

                # Get current orbit layer
                orbit_layer = self.orbit_layers[i]

                # Get layer attributes from tuple
                obstacle_size = orbit_layer[3]

                # Draw each obstacle
                for obstacle in self.obstacle_layers[i]:

                    obstacle_screen_position = obstacle - camera_position

                    # PLACEHOLDER: DRAW OBSTACLE
                    pygame.draw.circle(
                        window,
                        color=(255, 255, 255),
                        center=[obstacle_screen_position.x, obstacle_screen_position.y],
                        radius=obstacle_size
                        )

point_pool = [] # List of points the player can advance to
point_pool_size = 5 # Number of points in the pool
point_counter = 0 # Keeps track of the furthest point
point_index = 0 # The current point mapped to the correct point_pool index

vertical_point_spacing = 500 # The vertical spacing of the points
horizontal_point_spacing = 70 # The horizontal spacing of the points
point_radius = 55 # The radius of the points' circle
point_width = 5 # The width of the points' circle

# Point random generation, used to create "levels" of difficulty
random_difficulty_profiles = {
    0 : [              # 0th point threshold
        (2, 4),        # Point count random range
        (20, 60),      # Spread random range
        (100, 100),     # Distance random range
        (20, 30),      # Size random range
        (2, 5),    # Speed random range
        (0, 0),       # Sine speed amplitude random range
        (0, 0),       # Sine speed frequency random range
        (0, 0),        # Sine distance amplitude random range
        (0, 0),        # Sine distance frequency random range
        [1, 1]         # Number of layers
    ],
    10 : [             # 10th point threshold
        (2, 4),        # Point count random range
        (45, 60),      # Spread random range
        (70, 120),     # Distance random range
        (20, 30),      # Size random range
        (1, 1.5),    # Speed random range
        (5, 10),       # Sine speed amplitude random range
        (0, 50),       # Sine speed frequency random range
        (0, 0),        # Sine distance amplitude random range
        (0, 0),        # Sine distance frequency random range
        [1, 1]         # Number of layers
    ]
}

# CAMERA
camera_offset = Vector2(0, -300)
camera_speed = 4

return_value = None

# Function to get the position of the n'th point (point_number)
def get_point_position(point_number):
    global window
    global player_position
    global vertical_point_spacing
    return Vector2(uniform(player_position.x - horizontal_point_spacing, player_position.x + horizontal_point_spacing), point_number * -vertical_point_spacing)

# Function to get the needed velocity for the player to advance to the next point
def get_velocity():
    global point_pool
    global point_index
    global base_player_speed
    global player_position

    # Get direction towards player position and target position
    return normalize(point_pool[point_index].position - player_position) * base_player_speed

# Generates a random orbit
def generate_orbit():
    global point_counter
    global random_difficulty_profiles

    orbit = []

    current_profile = 0
    for key, value in random_difficulty_profiles.items():
        if key > current_profile and key <= point_counter:
            current_profile = key

    random_difficulty_profile = random_difficulty_profiles[current_profile]

    # [(count, spread, distance, size, base_speed, sine_speed_amp, sine_speed_freq, sine_distance_amp, sine_distance_freq)]
    # -1 index is last, which represents layer range
    layer_count = randint(random_difficulty_profile[-1][0], random_difficulty_profile[-1][1])
    for i in range(0, layer_count): 
        orbit.append([
            randint(random_difficulty_profile[0][0], random_difficulty_profile[0][1]),  # Count
            uniform(random_difficulty_profile[1][0], random_difficulty_profile[1][1]),  # Spread
            uniform(random_difficulty_profile[2][0], random_difficulty_profile[2][1]),  # Distance
            uniform(random_difficulty_profile[3][0], random_difficulty_profile[3][1]),  # Size
            uniform(random_difficulty_profile[4][0], random_difficulty_profile[4][1]),  # Base speed
            uniform(random_difficulty_profile[5][0], random_difficulty_profile[5][1]),  # Sine speed amp
            uniform(random_difficulty_profile[6][0], random_difficulty_profile[6][1]),  # Sine speed freq
            uniform(random_difficulty_profile[7][0], random_difficulty_profile[7][1]),  # Sine distance amp
            uniform(random_difficulty_profile[8][0], random_difficulty_profile[8][1]),  # Sine distance freq
        ])

    return orbit

# Function to start moving player to the next point
def advance_player():
    global current_point
    global point_index
    global player_state
    global point_pool
    global point_counter

    # Update indexes
    point_index += 1

    # Update player state to moving
    player_state = PlayerState.MOVING

    # Recycle "used" points
    if point_index > 1:
        # Set first point new position
        point_pool[0] = Point(position=get_point_position(point_counter + 1), orbit_layers=generate_orbit())

        # Rotate point list (first point now at last index)
        point_pool = point_pool[1:] + point_pool[:1]

        # Offset index
        point_index -= 1
        point_counter += 1

# Function to call when the player loses
def game_over():
    global score
    global player_state
    global player_velocity
    global window

    player_state = PlayerState.DEAD

    new_high_score = False
    # Check if high_score is in the dictionary
    if "high_score" in save.save_dict:
        high_score = save.save_dict["high_score"]
        if score > high_score:
            save.save_dict["high_score"] = score
            new_high_score = True
    else:
        save.save_dict["high_score"] = score
        new_high_score = True
    
    save.save_data()
    game_over_screen.load(window, score, new_high_score)

# Resets variables to allow replayability
def reset_state():
    global point_pool
    global point_counter
    global point_index
    global player_velocity
    global return_value
    global player_state
    global score
    point_pool = []
    point_counter = 0
    point_index = 0
    player_velocity = Vector2()
    return_value = None
    player_state = PlayerState.IDLE
    score = 0

# Function to the load the gameplay screen
def load(surface):
    global window
    global point_pool
    global player_position
    global player_state
    global camera_position
    global point_counter
    global camera_offset
    global score_value_text
    global score_text
    global return_value

    reset_state()

    window = surface

    score_text = Text(window,
                    text="Score",
                    font=FontPaths.NORMAL,
                    size=30,
                    color=(255, 255, 255),
                    text_anchor=Anchors.TOP_LEFT,
                    screen_anchor=Vector2(0.0, 0),
                    position=Vector2(10, 5)
                )

    score_value_text = Text(window,
                    text="0000",
                    font=FontPaths.EXTRA_BOLD,
                    size=100,
                    color=(255, 255, 255),
                    text_anchor=Anchors.TOP_LEFT,
                    screen_anchor=Vector2(0.0, 0),
                    position=Vector2(10, 20)
                )

    # Create 5 points for the pool
    for i in range(0, point_pool_size):
        point_pool.append(Point(position=get_point_position(point_counter + 1), orbit_layers=generate_orbit()))
        point_counter += 1
    
    # The first point should not have any obstacles as the player starts
    point_pool[0].obstacle_layers = []
    point_pool[0].orbit_layers = []

    # Set player position to first point
    player_position = point_pool[0].position

    # Set camera position to player position
    camera_position = player_position - Vector2(window.get_size()[0], window.get_size()[1]) / 2 - camera_offset 

# Function called every frame to update the game
def update(mouse_position, mouse_pressed, delta_time):

    # Bring necessary variables into scope
    global window
    global camera_position
    global player_velocity
    global player_position
    global camera_speed
    global player_state
    global point_pool
    global score
    global collection_particles
    global return_value

    # Only update current and next points, the rest are offscreen
    point_pool[point_index - 1].update(delta_time)
    point_pool[point_index].update(delta_time)
    point_pool[point_index + 1].update(delta_time)

    # Update particle collection pool
    for particle in collection_particles:
        direction = player_position - particle[0]
        sqr_distance = sqr_magnitude(direction)
        if sqr_distance < 10000:
            particle[0] = lerp(particle[0], player_position, delta_time * 10)
            particle[2] = lerp(particle[2], 0, delta_time * 5)
            if sqr_distance < 100 or particle[2] <= 1:
                # Remove particle if it is too close or too small
                if particle[2] <= 1 or sqr_magnitude(direction) < 100:
                    collection_particles.remove(particle)

                score += 10
        else:
            normalized_direction = normalize(direction)
            particle[1] += normalized_direction * 6000 * delta_time
            particle[0] += particle[1] * delta_time
            particle[2] -= delta_time * 3

    if player_state == PlayerState.IDLE:
        # If the player is idle, their velocity should be zero
        player_velocity = Vector2()

        # Slowly move to center of point
        player_position = lerp(player_position, point_pool[point_index].position, delta_time * 10)

        if mouse_pressed:
            advance_player()
    
    elif player_state == PlayerState.MOVING:
        # Update player velocity
        player_velocity = get_velocity()

        # Check if player is close enough to point to stop
        if sqr_magnitude(point_pool[point_index].position - player_position) < base_player_speed * 5:
            player_state = PlayerState.IDLE
            point_pool[point_index].cleared = True

            for obstacle_layer_index in range(0, len(point_pool[point_index].obstacle_layers)):
                for obstacle in point_pool[point_index].obstacle_layers[obstacle_layer_index]:
                    out_dir = normalize(obstacle - player_position)
                    rand_dir = Vector2(out_dir.y, -out_dir.x) * uniform(-2, 2)
                    collection_particles.append([obstacle,
                                                (out_dir + rand_dir) * 500,
                                                point_pool[point_index].orbit_layers[obstacle_layer_index][3]])
        
        # Initiate game over if player is too close
        if point_pool[point_index].get_sqr_distance(player_position) < 4000:
            game_over()
        
    elif player_state == PlayerState.DEAD:
        player_velocity = lerp(player_velocity, Vector2(), delta_time * 5)
        return_value = game_over_screen.update(delta_time, mouse_position, mouse_pressed)
        if return_value != None:
            return return_value

    # Update player position based on velocity
    player_position = player_position + player_velocity * delta_time
    
    score_string = str(score)
    if score_value_text.text != score_string:
        score_value_text.text = score_string
        score_value_text.update()

    # Finally update camera position
    window_size = Vector2(window.get_size()[0], window.get_size()[1])
    camera_position = lerp(camera_position, player_position - window_size / 2 + camera_offset, delta_time * camera_speed) 

# Function called to draw objects
def draw():
    global window
    global score
    global score_text
    global player_state
    global score_value_text

    window.fill((23, 22, 38))

    # Draw score
    score_text.draw()
    score_value_text.draw()

    # Draw collection particles
    for particle in collection_particles:
        particle_screen_position = particle[0] - camera_position
        pygame.draw.circle(
            window,
            color=(240, 240, 240),
            center=[particle_screen_position.x, particle_screen_position.y],
            radius=particle[2]
        )

    # Draw previous, current and next point, which are the only visible points
    for i in range(point_index - 1, point_index + 2):
        point_screen_position = point_pool[i].position - camera_position
        point_pool[i].draw(window, camera_position)

    # Draw player
    player_screen_position = player_position - camera_position
    pygame.draw.circle(
        window,
        color=(255, 0, 0),
        center=[player_screen_position.x, player_screen_position.y],
        radius=20
    )

    if player_state == PlayerState.DEAD:
        game_over_screen.draw()