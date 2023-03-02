import pygame
import sys
import sprite_sheet
import random
import time as t

from pygame import *

# Inicializar Pygame
pygame.init()

random.seed(t.time)

# Constantes para una mejor legibilidad

# Direcciones
IZQUIERDA = 0
DERECHA = 1
ARRIBA = 2
ABAJO = 3

# Definir el tamaño de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Definir las coordenadas y dimensiones del rectángulo de la banda horizontal
BAND_LEFT = 0
BAND_TOP = SCREEN_HEIGHT - 100
BAND_WIDTH = SCREEN_WIDTH
BAND_HEIGHT = 100

# Definir el color de la banda horizontal
BAND_COLOR = (0, 255, 0)  # verde

# Velocidad de movimiento de la rana (en píxeles por segundo)
FROG_SPEED = 10

# Velocidades en cada dirección (izquierda, derecha, arriba, abajo)
FROG_SPEEDS = [0, 0, 0, 0]

#Tamaño de la rana
FROG_SIZE = (int(BAND_HEIGHT * 0.4), int(BAND_HEIGHT * 0.4))
#frog_image = pygame.transform.scale(frog_image, FROG_SIZE)

# Obtener las coordenadas iniciales de la rana
FROG_X = int(SCREEN_WIDTH / 2 - FROG_SIZE[0] / 2)
FROG_Y = BAND_TOP + int(BAND_HEIGHT / 2) - int(FROG_SIZE[1] / 2)

# A donde está mirando la rana
lookingAt = ARRIBA

# Mecanica de salto

MAX_TIME = 2    # Tiempo[s] tras el cual seguir cargando el salto, no tiene efecto
MAX_JUMP_DISTANCE = FROG_SIZE[0] * 2
JUMP_VELOCITY = 10
isJumping = False
isLoadingJump = False
pos_final = (0,0)
avance = (0,0)

clock = pygame.time.Clock()

# Crear la ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Establecer el título de la ventana
pygame.display.set_caption("Smart Frog")

# Cargar imagen de fondo (agua)
background_image = pygame.image.load('water_tile.jpg')

# Crear capa de fondo
background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background_surface = background_surface.convert()

# Rellenar capa de fondo con la imagen
for x in range(0, SCREEN_WIDTH, background_image.get_width()):
    for y in range(0, SCREEN_HEIGHT, background_image.get_height()):
        background_surface.blit(background_image, (x, y))

# Cargar la imagen de la rana
#frog_image = pygame.image.load("frog.png")

#girar una imagen 180 grados       
#frog_image = pygame.transform.rotate(frog_image, 180)

#hoja de sprites
sprite_sheet_image = pygame.image.load('sprites_rana.png').convert_alpha()    
sprite_sheet = sprite_sheet.SpriteSheet(sprite_sheet_image) 

#Tiempo que transcurre entre cada sprite del movimiento de la rana
cooldown = 150

#Para actualizar la animacion de los sprites de la rana
last_update = pygame.time.get_ticks()

#lista de sprites
spritelist = []
#indice para recorrer la lista de sprites
sprite = 0

#añado a la lista de sprites el sprite con el que empieza la rana 
spritelist.append(sprite_sheet.get_image(1, 3, 48, 48, 1))

def debug_frog():
    print("")

def posicionSalto(distance, direction):
    avance = (JUMP_VELOCITY / 60)
    if direction == ARRIBA:
        return ((FROG_X, max(0, FROG_Y-distance)), (0, -avance))
    if direction == ABAJO:
        return ((FROG_X, min(SCREEN_HEIGHT, FROG_Y+distance)), (0, avance))
    if direction == DERECHA:
        return ((min(FROG_X, FROG_X + distance), FROG_Y), (avance, 0))
    if direction == IZQUIERDA:
        return ((max(FROG_X, FROG_X - distance), FROG_Y), (-avance, 0))

def reachedPosition(actual_pos, final_pos, direction):
    if direction == ARRIBA:
        return actual_pos[1]<=final_pos[1]
    if direction == ABAJO:
        return actual_pos[1]>=final_pos[1]
    if direction == DERECHA:
        return actual_pos[0]>=final_pos[0]
    if direction == IZQUIERDA:
        return actual_pos[0]<=final_pos[0]

# Game loop
while True:

    #Imprimo toda la hoja de sprites
    #screen.blit(sprite_sheet_image,(0,0))      

    #imprimo sprite de la hoja de sprites en la posición (0,0) del mapa
    #screen.blit(sprite_00, (0,0))

    if isJumping:
        # Ha acabado de saltar?
        if reachedPosition((FROG_X, FROG_Y), (pos_final), lookingAt):
            (FROG_X, FROG_Y) = pos_final
            isJumping = False
        else:
            # Borro todos los eventos
            event.clear()
            FROG_X += avance[0]
            FROG_Y += avance[1]
    else:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Detectar las teclas de dirección presionadas y establecer la velocidad en la dirección correspondiente
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    print("Space down")
                    isLoadingJump = True
                    clock.tick()
                elif evento.key == pygame.K_LEFT:
                    # La rana se queda mirando hacia la izquierda
                    lookingAt = IZQUIERDA
                    spritelist.clear()
                    if not isLoadingJump:
                        FROG_SPEEDS[0] = -FROG_SPEED
                    #añado sprite de la columna 0 y fila 1 y otro de columna 1 y fila 1 
                    #para hacer la animación cuando se mueve a la izquierda 
                    spritelist.append(sprite_sheet.get_image(0, 1, 48, 48, 1))
                    spritelist.append(sprite_sheet.get_image(1, 1, 48, 48, 1))                      
                elif evento.key == pygame.K_RIGHT:
                    # La rana se queda mirando hacia la derecha
                    lookingAt = DERECHA
                    spritelist.clear()
                    if not isLoadingJump:
                        FROG_SPEEDS[1] = FROG_SPEED
                    spritelist.append(sprite_sheet.get_image(0, 2, 48, 48, 1))
                    spritelist.append(sprite_sheet.get_image(1, 2, 48, 48, 1))                
                elif evento.key == pygame.K_UP:
                    # La rana se queda mirando hacia arriba
                    lookingAt = ARRIBA
                    spritelist.clear()
                    if not isLoadingJump:
                        FROG_SPEEDS[2] = -FROG_SPEED
                    spritelist.append(sprite_sheet.get_image(0, 3, 48, 48, 1))
                    spritelist.append(sprite_sheet.get_image(1, 3, 48, 48, 1))                       
                elif evento.key == pygame.K_DOWN:
                    # La rana se queda mirando hacia abajo
                    lookingAt = ABAJO
                    spritelist.clear()
                    if not isLoadingJump:
                        FROG_SPEEDS[3] = FROG_SPEED
                    spritelist.append(sprite_sheet.get_image(0, 0, 48, 48, 1))
                    spritelist.append(sprite_sheet.get_image(1, 0, 48, 48, 1))        
            # Detectar las teclas de dirección liberadas y establecer la velocidad en la dirección correspondiente a cero
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    t1_jump = clock.tick()
                    # Math: \min (max_{jump\ distance}, \frac{t_1 - t_0}{max_{time}} \times max_{jumpeable\ distance})
                    jump_distance = ((t1_jump / 1000) / MAX_TIME) * MAX_JUMP_DISTANCE
                    jump_distance = min(MAX_JUMP_DISTANCE, jump_distance)
                    print("Space up")
                    print("t1: " + (t1_jump / 1000).__str__())
                    print("Frog size: " + FROG_SIZE.__str__())
                    print("Distance to jump: " + jump_distance.__str__())
                    isJumping = True
                    isLoadingJump = False
                    pos_final, avance = posicionSalto(jump_distance, lookingAt)
                elif evento.key == pygame.K_LEFT:
                    FROG_SPEEDS[0] = 0
                elif evento.key == pygame.K_RIGHT:
                    FROG_SPEEDS[1] = 0
                elif evento.key == pygame.K_UP:
                    FROG_SPEEDS[2] = 0
                elif evento.key == pygame.K_DOWN:
                    FROG_SPEEDS[3] = 0

        # Calcular la posición de la rana en cada cuadro
        FROG_X += (FROG_SPEEDS[1] + FROG_SPEEDS[0]) / 60
        FROG_Y += (FROG_SPEEDS[3] + FROG_SPEEDS[2]) / 60

    # Limitar la posición de la rana a la banda horizontal y al ancho de pantalla
    if FROG_X < 0:
        FROG_X = 0
    elif FROG_X > SCREEN_WIDTH - FROG_SIZE[0]:
        FROG_X = SCREEN_WIDTH - FROG_SIZE[0]

    if not isJumping:
        if FROG_Y < BAND_TOP:
            FROG_Y = BAND_TOP
        elif FROG_Y > SCREEN_HEIGHT - FROG_SIZE[1]:
            FROG_Y = SCREEN_HEIGHT - FROG_SIZE[1]

    # Dibujar capa de fondo
    screen.blit(background_surface, (0, 0))

    # Dibujar la banda horizontal
    pygame.draw.rect(screen, BAND_COLOR, (BAND_LEFT, BAND_TOP, BAND_WIDTH, BAND_HEIGHT))
    
    ##TODO esto debe ocurrir solo mientras una tecla está presionada, cuando no hay una tecla presionada printear el ultimo elemento de la sprite list
    quieto = 0

    if(FROG_SPEEDS[0] == 0 and FROG_SPEEDS[1] == 0 and FROG_SPEEDS[2] == 0 and FROG_SPEEDS[3] == 0):
        quieto = 1

    current_time = pygame.time.get_ticks()
    if (current_time-last_update >= cooldown and quieto == 0):
        sprite += 1
        last_update = current_time
        if sprite >= len(spritelist):
            sprite = 0
    
    if (quieto==1):
        sprite = len(spritelist)-1

    # Dibujar la imagen de la rana en la pantalla
    screen.blit(spritelist[sprite], (FROG_X, FROG_Y))

    # Actualizar la pantalla
    pygame.display.update()


