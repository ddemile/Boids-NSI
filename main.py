import pyxel
import random
import math
import time

# http://www.kfish.org/boids/pseudocode.html

LARGEUR = 160 * 1
HAUTEUR = 120 * 1
NB_BOIDS = 400

MAX_SPEED = 1.5
VISION = 10

COHESION_FACTOR = 1
SEPARATION_FACTOR = 1
ALIGNMENT_FACTOR = 1

# Types
Vec = list[float] | tuple[float, float]
Boid = list[float | int]

boids: list[Boid] = []

start_time = time.time()
fps_gap = 0
counter = 0

def init_boids():
    for _ in range(NB_BOIDS):
        x = random.uniform(0, LARGEUR)
        y = random.uniform(0, HAUTEUR)
        vx = random.uniform(-MAX_SPEED, MAX_SPEED)
        vy = random.uniform(-MAX_SPEED, MAX_SPEED)
        boids.append([x, y, vx, vy, random.randrange(0, 8)])

# Utilities

def mutliply(vec: Vec, mult: float):
    return (vec[0] * mult, vec[1] * mult)

def length(x: float, y: float) -> float:
    return math.hypot(x, y)
    
def normalize(vec: Vec):
    vx = vec[0]
    vy = vec[1]
 
    vec_length = length(vx, vy)
    if vec_length > 0:
        vx /= vec_length
        vy /= vec_length

    return (vx, vy)
    

def limit_velocity(vel: Vec) -> Vec:
    vx = vel[0]
    vy = vel[1]

    len = length(vel[0], vel[1])

    if len > MAX_SPEED:
        vx, vy = normalize(vel)
        vx *= MAX_SPEED
        vy *= MAX_SPEED

    return (vx, vy)
    
# Grid

def build_grid(positions: list[Boid], cell_size: int):
    grid = dict[tuple[int, int], list]()
    for i in range(len(positions)):
        boid = positions[i]
        x, y = boid[0], boid[1]
        cx, cy = int(x //cell_size), int(y // cell_size)
        position = (cx, cy)
        if not position in grid:
            grid[position] = []
        grid[position].append(i)
    return grid

def get_neighbours(b1: Boid, boids: list[Boid], grid: dict[tuple[int, int], list], radius: int, cell_size: int):
    cx, cy = int(b1[0] // cell_size), int(b1[1] // cell_size)
    neighbours = []
    squared_distances = []

    squared_radius = radius ** 2

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for i in grid.get((cx + dx, cy + dy), []):
                b2 = boids[i]
                if b1 != b2:
                    squared_distance = (b1[0] - b2[0]) ** 2 + (b1[1] - b2[1]) ** 2
                    if squared_distance < squared_radius:
                        neighbours.append(b2)
                        squared_distances.append(squared_distance)
    return neighbours, squared_distances

# Rules

def apply_rules(b1: Boid, neighbours: list[Boid], squared_distances: list[float]):
    cohesion = [0.0, 0.0]
    separation = [0.0, 0.0]
    alignment = [0.0, 0.0]

    if len(neighbours) > 0:
        for i in range(len(neighbours)):
            b2 = neighbours[i]

            # Cohesion
            cohesion[0] += b2[0]
            cohesion[1] += b2[1]

            # Separation
            if squared_distances[i] < 2 ** 2:
                separation[0] -= b2[0] - b1[0]
                separation[1] -= b2[1] - b1[1]

            # Alignement
            alignment[0] += b2[2]
            alignment[1] += b2[3]

        # Cohesion
        cohesion[0] /= len(neighbours)
        cohesion[1] /= len(neighbours)
        cohesion = ((cohesion[0] - b1[0]) / 100, (cohesion[1] - b1[1]) / 100)

        # Alignment
        alignment[0] /= len(neighbours)
        alignment[1] /= len(neighbours)

        alignment[0] = (alignment[0] - b1[2]) / 8
        alignment[1] = (alignment[1] - b1[3]) / 8

    return cohesion, separation, alignment

def tend_to_place(boid: Boid, place: Vec):
    return ((place[0] - boid[0]) / 100, (place[1] - boid[1]) / 100)

# Edge behaviour

def warp(boid: Boid):
    if boid[0] < 0:
        boid[0] = LARGEUR - 1
    elif boid[0] >= LARGEUR:
        boid[0] = 0
    if boid[1] < 0:
        boid[1] = HAUTEUR - 1
    elif boid[1] >= HAUTEUR:
        boid[1] = 0

def bounce(boid: Boid):
    if boid[0] < 0:
        boid[0] = 0
        boid[2] *= -1
    elif boid[0] >= LARGEUR:
        boid[0] = LARGEUR - 1
        boid[2] *= -1
    if boid[1] < 0:
        boid[1] = 0
        boid[3] *= -1
    elif boid[1] >= HAUTEUR:
        boid[1] = HAUTEUR - 1
        boid[3] *= -1

def bound(boid: Boid):
    vel = [0.0, 0.0]

    force = 0.25

    if boid[0] < 0:
        vel[0] = force
    elif boid[0] >= LARGEUR:
        vel[0] = -force
    if boid[1] < 0:
        vel[1] = force
    elif boid[1] >= HAUTEUR:
        vel[1] = -force
    
    return vel
 
def update_boids():
    grid = build_grid(boids, int(VISION / 2))
    for boid in boids:
        neighbours, squared_distances = get_neighbours(boid, boids, grid, VISION, int(VISION / 2))

        cohesion, separation, alignment = apply_rules(boid, neighbours, squared_distances)
        
        mouse = (pyxel.mouse_x - boid[0], pyxel.mouse_y - boid[1])
        mouse = normalize(mouse)

        cohesion = mutliply(cohesion, COHESION_FACTOR)
        separation = mutliply(separation, SEPARATION_FACTOR)
        alignment = mutliply(alignment, ALIGNMENT_FACTOR)
        mouse = mutliply(mouse, 0)

        vx = cohesion[0] + separation[0] + alignment[0] + mouse[0]
        vy = cohesion[1] + separation[1] + alignment[1] + mouse[1]

        bound_force = bound(boid)
        vx += bound_force[0]
        vy += bound_force[1]
        
        boid[2] += vx
        boid[3] += vy

        vx, vy = limit_velocity((boid[2], boid[3]))
        
        boid[2] = vx
        boid[3] = vy

        # bounce(boid)
        # warp(boid)
        
        # Apply velocity
        boid[0] += boid[2]
        boid[1] += boid[3]

def draw_boids():
    for b in boids:
        pyxel.pset(int(b[0]), int(b[1]), 7)
    
def update():
    pyxel.cls(0)
    update_boids()

def draw():
    global start_time, counter

    draw_boids()
    pyxel.pset(pyxel.mouse_x, pyxel.mouse_y, 4)

    counter+=1
    if (time.time() - start_time) > fps_gap * 1000:
        pyxel.title(f"FPS: {int(counter / (time.time() - start_time))}")
        counter = 0
        start_time = time.time()

init_boids()
pyxel.init(LARGEUR, HAUTEUR)
pyxel.run(update, draw)