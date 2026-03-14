import pyxel
import random
import math
import time
from collections.abc import Callable

# http://www.kfish.org/boids/pseudocode.html

# Constantes

WIDTH = 512
HEIGHT = 300
NB_BOIDS = 600

SIMULATION_WIDTH = WIDTH / 2
SIMULATION_HEIGHT = HEIGHT / 2

MAX_SPEED = 1.5
VISION = 12

COHESION_FACTOR = 1
SEPARATION_FACTOR = 1
ALIGNMENT_FACTOR = 1

UI_MARGIN = 4
PANEL_PADDING = 5
PANEL_WIDTH = 100
RADIO_BUTTON_RADIUS = 4
RADIO_BUTTONS_Y_OFFSET = 100
RADIO_BUTTONS_GAP = 12

DEBUG_MODE = False

# Types

Vec = list[float] | tuple[float, float]
Boid = list[float | int]

# Utilitaires

def mutliply(vec: Vec, mult: float):
    """Multiple un vecteur avec le facteur 'mult'"""
    return (vec[0] * mult, vec[1] * mult)

def length(x: float, y: float) -> float:
    """Renvoie la longueur d'un vecteur"""
    return math.hypot(x, y)
    
def text_width(text):
    """Renvoie la taille d'une chaine de caractères en pixels"""
    return len(text) * 4 - 1

def normalize(vec: Vec):
    """Renvoie la version normalisée d'un vecteur"""
    vx = vec[0]
    vy = vec[1]
 
    vec_length = length(vx, vy)
    if vec_length > 0:
        vx /= vec_length
        vy /= vec_length

    return (vx, vy)
    

def limit_velocity(vel: Vec) -> Vec:
    """Empêche la valeur d'entrée 'vel' de dépasser la constante 'MAX_SPEED'"""
    vx = vel[0]
    vy = vel[1]

    len = length(vel[0], vel[1])

    if len > MAX_SPEED:
        vx, vy = normalize(vel)
        vx *= MAX_SPEED
        vy *= MAX_SPEED

    return (vx, vy)

def ease_in_out_back(x: float):
    """Prend une valeur entre 0 et 1 et retourne une valeur interpolée avec easing (accélération puis décélération), destinée aux animations"""
    c1 = 1.70158
    c2 = c1 * 1.525

    return (pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2 if x < 0.5 else (pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2

def lerp(a: float, b: float, t: float) -> float:
    """Intérpolation linéaire"""
    return (1 - t) * a + t * b

def inv_lerp(a: float, b: float, v: float) -> float:
    """Intérpolation linéaire inversée"""
    return (v - a) / (b - a)

# Grille

def build_grid(positions: list[Boid], cell_size: int):
    """Créée une grille contenant les boids"""
    grid = dict[tuple[int, int], list]()
    for i in range(len(positions)):
        boid = positions[i]
        x, y = boid[0], boid[1]
        cx, cy = int(x // cell_size), int(y // cell_size)
        position = (cx, cy)
        if not position in grid:
            grid[position] = []
        grid[position].append(i)
    return grid

def get_neighbours(b1: Boid, boids: list[Boid], grid: dict[tuple[int, int], list], radius: int, cell_size: int):
    """Renvoie la liste de tous les voisins d'un boid"""
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

# Règles

def apply_rules(b1: Boid, neighbours: list[Boid], squared_distances: list[float]):
    """Applique les trois régles fondamentales du flocking : cohésion, séparation, alignement"""
    cohesion = [0.0, 0.0]
    separation = [0.0, 0.0]
    alignment = [0.0, 0.0]

    if len(neighbours) > 0:
        for i in range(len(neighbours)):
            b2 = neighbours[i]

            # Cohésion
            cohesion[0] += b2[0]
            cohesion[1] += b2[1]

            # Séparation
            if squared_distances[i] < 2 ** 2:
                separation[0] -= b2[0] - b1[0]
                separation[1] -= b2[1] - b1[1]

            # Alignement
            alignment[0] += b2[2]
            alignment[1] += b2[3]

        # Cohésion
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
    """Dirige le boid vers des coordonées spécifiques"""
    return ((place[0] - boid[0]) / 100, (place[1] - boid[1]) / 100)

# Comportement au niveau des bords

def warp(boid: Boid):
    """Si le boid touche le bord de l'écran il se téléporte au coin opposé"""
    if boid[0] < 0:
        boid[0] = SIMULATION_WIDTH - 1
    elif boid[0] >= SIMULATION_WIDTH:
        boid[0] = 0
    if boid[1] < 0:
        boid[1] = SIMULATION_HEIGHT - 1
    elif boid[1] >= SIMULATION_HEIGHT:
        boid[1] = 0

def bounce(boid: Boid):
    """Si le boid touche le bord de l'écran il rebondit sur ce-dernier"""
    if boid[0] < 0:
        boid[0] = 0
        boid[2] *= -1
    elif boid[0] >= SIMULATION_WIDTH:
        boid[0] = SIMULATION_WIDTH - 1
        boid[2] *= -1
    if boid[1] < 0:
        boid[1] = 0
        boid[3] *= -1
    elif boid[1] >= SIMULATION_HEIGHT:
        boid[1] = SIMULATION_HEIGHT - 1
        boid[3] *= -1

def bound(boid: Boid):
    """Si le boid quitte la zone de jeu il va se diriger vers celle-ci"""
    vel = [0.0, 0.0]

    force = 0.25

    if boid[0] < 0:
        vel[0] = force
    elif boid[0] >= SIMULATION_WIDTH:
        vel[0] = -force
    if boid[1] < 0:
        vel[1] = force
    elif boid[1] >= SIMULATION_HEIGHT:
        vel[1] = -force
    
    return vel

# Fonctions pour la logique de l'application
 
def update_boids():
    """Met à jour la position et la vitesse de tous les boids en appliquant les règles du flocking"""
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

        if selected_edge_behaviour == 2:
            bound_force = bound(boid)
            vx += bound_force[0]
            vy += bound_force[1]
        
        boid[2] += vx
        boid[3] += vy

        vx, vy = limit_velocity((boid[2], boid[3]))
        
        boid[2] = vx
        boid[3] = vy

        if selected_edge_behaviour == 0:
            warp(boid)
        elif selected_edge_behaviour == 1:
            bounce(boid)
        
        # Apply velocity
        boid[0] += boid[2]
        boid[1] += boid[3]

def update_sliders():
    """Actualise tous les sliders"""
    for slider in sliders:
        slider_x = UI_MARGIN + PANEL_PADDING
        slider_y = UI_MARGIN + PANEL_PADDING + slider["y_offset"]
        handle_x = slider_x + slider["width"] * slider["value"]
        hovered = pyxel.mouse_x >= handle_x - 2 and pyxel.mouse_x <= handle_x + 2 and pyxel.mouse_y >= slider_y - 2 and pyxel.mouse_y <= slider_y + 2
        slider["hovered"] = hovered
        if not slider["dragged"] and hovered and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            slider["dragged"] = True
        elif slider["dragged"] and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            slider["dragged"] = False
        if slider["dragged"]:
            slider["value"] = min(max((pyxel.mouse_x - slider_x) / slider["width"], 0), 1)
            slider["callback"](lerp(slider["min_value"], slider["max_value"], slider["value"]))

def update_radio_buttons():
    """Actualise le groupe de boutons permettant de choisir le comportement aux bords de l'écran"""
    global radio_buttons, selected_edge_behaviour
    radio_buttons = []

    pos = UI_MARGIN + PANEL_PADDING + RADIO_BUTTON_RADIUS

    for i in range(len(edge_behaviours)):
        y_pos = pos + RADIO_BUTTONS_Y_OFFSET + i * RADIO_BUTTONS_GAP

        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            distance = length(pyxel.mouse_x - pos, pyxel.mouse_y - y_pos)

            if distance < 5:
                selected_edge_behaviour = i
                break

def update_ui():
    """Actualise l'interface utilisateur"""

    global COHESION_FACTOR, opening_ui, ui_progress

    if opening_ui:
        ui_progress -= 1 / 30
    else:
        ui_progress += 1 / 30

    ui_progress = min(max(ui_progress, 0), 1)

    if pyxel.btnr(pyxel.KEY_SPACE):
        opening_ui = not opening_ui
        
    if ui_progress > 0:
        update_sliders()
        update_radio_buttons()

    total_panel_width = PANEL_WIDTH + UI_MARGIN
    content_x_pos = ease_in_out_back(ui_progress) * total_panel_width - total_panel_width

    # Vérifie si le bouton de basculement de visibilité de l'interface utilisateur est survolé
    toggle_button[4] = pyxel.mouse_x >= content_x_pos + toggle_button[0] and pyxel.mouse_x <= content_x_pos + toggle_button[0] + toggle_button[2] and pyxel.mouse_y >= toggle_button[1] and pyxel.mouse_y <= toggle_button[1] + toggle_button[3]

    if toggle_button[4] and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
        opening_ui = not opening_ui

def update():
    """Boucle principale de mise à jour appelée à chaque frame"""
    pyxel.cls(3)
    update_boids()
    update_ui()

# Fonctions pour l'affichage

def draw_boids():
    """Affiche les boids"""
    scale_factor_x, scale_factor_y = WIDTH / SIMULATION_WIDTH, HEIGHT / SIMULATION_HEIGHT
    for b in boids:
        x, y = int(b[0] * scale_factor_x), int(b[1] * scale_factor_y)
        pyxel.rect(x, y, scale_factor_x, scale_factor_y, 7)

def draw_sliders(content_pos: Vec):
    """Affiche les sliders ainsi que leur étiquette"""
    for slider in sliders:
        y_pos = content_pos[1] + slider["y_offset"]

        # Affiche l'étiquette du slider
        value = lerp(slider["min_value"], slider["max_value"], slider["value"])
        if value < 100:
            value = round(value, 2)
        else:
            value = round(value)
        pyxel.text(content_pos[0], y_pos - 9, f"{slider["label"]} : {value}", 1)

        # Affiche la barre du slider
        pyxel.line(
            content_pos[0], y_pos, 
            content_pos[0] + slider["width"], y_pos,
            3
        )

        # Affcihe le curseur du slider
        handle_color = 4 if slider["dragged"] else 3 if slider["hovered"] else 2
        pyxel.rect(content_pos[0] + math.floor(slider["width"] * slider["value"]) - 2, y_pos - 2, 5, 5, handle_color)
    
def draw_radio_buttons(content_pos: Vec):
    """Affiche le groupe de boutons permettant de choisir le comportement aux bords de l'écran"""
    radius = 4
    for i in range(len(edge_behaviours)):
        name = edge_behaviours[i]
        y_pos = content_pos[1] + RADIO_BUTTONS_Y_OFFSET + i * RADIO_BUTTONS_GAP
        pyxel.circ(content_pos[0] + radius, y_pos + radius, radius, 3)
        if i == selected_edge_behaviour:
            pyxel.circ(content_pos[0] + radius, y_pos + radius, radius - 1, 1)
        pyxel.text(content_pos[0] + 8 + 3, y_pos + radius - 5 / 2, name, 1)

def draw_ui(pos: Vec):
    """Affiche tous les éléments de l'interface utilisateur"""
    content_pos = (pos[0] + UI_MARGIN + PANEL_PADDING, pos[1] + UI_MARGIN + PANEL_PADDING)

    # Affiche le panneau de l'interface
    pyxel.rectb(pos[0] + UI_MARGIN, pos[1] + UI_MARGIN, PANEL_WIDTH, HEIGHT - UI_MARGIN * 2, 4)
    pyxel.rect(pos[0] + UI_MARGIN + 1, pos[1] + UI_MARGIN + 1, PANEL_WIDTH - 2, HEIGHT - (UI_MARGIN + 1) * 2, 5)

    draw_sliders(content_pos)
    pyxel.text(content_pos[0], RADIO_BUTTONS_Y_OFFSET + 1, "Comportement aux bords", 1)
    draw_radio_buttons(content_pos)

def draw():
    """Boucle principale de rendu appelée à chaque frame"""
    global start_time, counter, fps, ui_progress

    draw_boids()

    total_panel_width = PANEL_WIDTH + UI_MARGIN
    content_x_pos = ease_in_out_back(ui_progress) * total_panel_width - total_panel_width

    if ui_progress > 0:
        draw_ui([content_x_pos, 0])

    # Affiche le bouton de basculement de visibilité du panneau de l'interface utilisateur
    pyxel.rectb(content_x_pos + toggle_button[0], toggle_button[1], toggle_button[2], toggle_button[3], 5 if toggle_button[4] else 4)
    pyxel.rect(content_x_pos + toggle_button[0] + 1, toggle_button[1] + 1, toggle_button[2] - 2, toggle_button[3] - 2, 6 if toggle_button[4] else 5)
    # pyxel.text(content_x_pos + UI_MARGIN + PANEL_WIDTH + 4 + 2, UI_MARGIN + 2, toggle_button[4], 1)
    pyxel.blt(content_x_pos + UI_MARGIN + PANEL_WIDTH + 4 + 2, UI_MARGIN + 2, 0, 8, 0, 13, 13, 0)

    
    # Affiche le curseur
    pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, 0, 0, 8, 8, 0)

    # Calcule et affiche le nombre d'images par seconde si le mode de débogage est activé
    if DEBUG_MODE:
        counter += 1
        if (time.time() - start_time) > fps_gap * 1000:
            fps = int(counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()
        pyxel.text(4, 4, f"FPS: {fps}", 8)

# Initialisation des éléments

def make_sliders(sliders_def: list[tuple[str, int, int, float, float, float, Callable[[float], None]]]):
    """Crée la structure interne des sliders à partir de leurs définitions"""
    sliders = []
    for slider_def in sliders_def:
        sliders.append({
            "label": slider_def[0],
            "y_offset": slider_def[1],
            "width": slider_def[2],
            "value": inv_lerp(slider_def[4], slider_def[5], slider_def[3]),
            "min_value": slider_def[4],
            "max_value": slider_def[5],
            "callback": slider_def[6],
            "hovered": False,
            "dragged": False
        })
    return sliders

def init_boids():
    """Initialise la liste de boids avec des positions et velocités aléatoires"""
    for _ in range(NB_BOIDS):
        x = random.uniform(0, SIMULATION_WIDTH)
        y = random.uniform(0, SIMULATION_HEIGHT)
        vx = random.uniform(-MAX_SPEED, MAX_SPEED)
        vy = random.uniform(-MAX_SPEED, MAX_SPEED)
        boids.append([x, y, vx, vy, random.randrange(0, 8)])

def update_boids_count(new_count):
    """Ajoute ou supprime des boids afin d'atteindre le nombre demandé"""

    global NB_BOIDS, boids
    diff = new_count - NB_BOIDS

    if diff > 0:
        for _ in range(int(diff)):
            x = random.uniform(0, SIMULATION_WIDTH)
            y = random.uniform(0, SIMULATION_HEIGHT)
            vx = random.uniform(-MAX_SPEED, MAX_SPEED)
            vy = random.uniform(-MAX_SPEED, MAX_SPEED)
            boids.append([x, y, vx, vy, random.randrange(0, 8)])
    else:
        boids = boids[:int(new_count)]

    NB_BOIDS = new_count


# Programme principal

boids: list[Boid] = []

start_time = time.time()
fps_gap = 0
counter = 0
fps = 0

ui_progress = 1
opening_ui = False
# [pos_x, pos_y, width, height, hovered]
toggle_button = [UI_MARGIN + PANEL_WIDTH + 4, UI_MARGIN, 17, 17, False]

sliders = make_sliders([
    # (label, y_offset, width, default_value (between min_value and max_value), min_value, max_value, callback)
    ("Cohesion", 9, PANEL_WIDTH - PANEL_PADDING * 2 - 1, COHESION_FACTOR, 0, 5, lambda value: globals().__setitem__("COHESION_FACTOR", value)),
    ("Separation", 15 + 9, PANEL_WIDTH - PANEL_PADDING * 2 - 1, SEPARATION_FACTOR, 0, 5, lambda value: globals().__setitem__("SEPARATION_FACTOR", value)),
    ("Alignement", 30 + 9, PANEL_WIDTH - PANEL_PADDING * 2 - 1, ALIGNMENT_FACTOR, 0, 5, lambda value: globals().__setitem__("ALIGNMENT_FACTOR", value)),
    ("Vitesse max", 45 + 9, PANEL_WIDTH - PANEL_PADDING * 2 - 1, MAX_SPEED, 0, 10, lambda value: globals().__setitem__("MAX_SPEED", value)),
    ("Vision", 60 + 9, PANEL_WIDTH - PANEL_PADDING * 2 - 1, VISION, 5, 50, lambda value: globals().__setitem__("VISION", value)),
    ("Nombre de boids", 75 + 9, PANEL_WIDTH - PANEL_PADDING * 2 - 1, NB_BOIDS, 100, 1000, update_boids_count)
])

radio_buttons = []

edge_behaviours = [
    "Torique",
    "Rebondir",
    "Revenir"
]
selected_edge_behaviour = 2

init_boids()
pyxel.init(WIDTH, HEIGHT)
pyxel.load("res.pyxres")
pyxel.load_pal("pal.txt")
pyxel.title("Simulation de boids")
pyxel.run(update, draw)