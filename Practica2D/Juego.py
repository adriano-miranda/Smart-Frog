import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Crear la ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Establecer el título de la ventana
pygame.display.set_caption("Smart Frog")

# Definir el color de la banda horizontal
BAND_COLOR = (0, 255, 0)  # verde

# Definir las coordenadas y dimensiones del rectángulo de la banda horizontal
BAND_LEFT = 0
BAND_TOP = SCREEN_HEIGHT - 100
BAND_WIDTH = SCREEN_WIDTH
BAND_HEIGHT = 100

# Cargar la imagen de la rana
frog_image = pygame.image.load("frog.png")

# Cargar imagen de fondo
background_image = pygame.image.load('water_tile.jpg')

# Crear capa de fondo
background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background_surface = background_surface.convert()

# Rellenar capa de fondo con la imagen
for x in range(0, SCREEN_WIDTH, background_image.get_width()):
    for y in range(0, SCREEN_HEIGHT, background_image.get_height()):
        background_surface.blit(background_image, (x, y))

#Tamaño de la rana
FROG_SIZE = (int(BAND_HEIGHT * 0.4), int(BAND_HEIGHT * 0.4))
frog_image = pygame.transform.scale(frog_image, FROG_SIZE)

# Obtener las coordenadas iniciales de la rana
FROG_X = int(SCREEN_WIDTH / 2 - FROG_SIZE[0] / 2)
FROG_Y = BAND_TOP + int(BAND_HEIGHT / 2) - int(FROG_SIZE[1] / 2)

# Velocidad de movimiento de la rana (en píxeles por segundo)
FROG_SPEED = 10

# Velocidades en cada dirección (izquierda, derecha, arriba, abajo)
FROG_SPEEDS = [0, 0, 0, 0]

#comienza mirando para arriba        
frog_image = pygame.transform.rotate(frog_image, 180)

        
# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Detectar las teclas de dirección presionadas y establecer la velocidad en la dirección correspondiente
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                FROG_SPEEDS[0] = -FROG_SPEED
                frog_image = pygame.image.load("frog.png")
                frog_image = pygame.transform.scale(frog_image, FROG_SIZE)
                frog_image = pygame.transform.rotate(frog_image, 270)
            
            elif event.key == pygame.K_RIGHT:
                FROG_SPEEDS[1] = FROG_SPEED
                frog_image = pygame.image.load("frog.png")
                frog_image = pygame.transform.scale(frog_image, FROG_SIZE)
                frog_image = pygame.transform.rotate(frog_image, 90)
            elif event.key == pygame.K_UP:
                FROG_SPEEDS[2] = -FROG_SPEED
                frog_image = pygame.image.load("frog.png")
                frog_image = pygame.transform.scale(frog_image, FROG_SIZE)
                frog_image = pygame.transform.rotate(frog_image, 180)
            elif event.key == pygame.K_DOWN:
                FROG_SPEEDS[3] = FROG_SPEED
                frog_image = pygame.image.load("frog.png")
                frog_image = pygame.transform.scale(frog_image, FROG_SIZE)
                frog_image = pygame.transform.rotate(frog_image, 0)
                
            


        # Detectar las teclas de dirección liberadas y establecer la velocidad en la dirección correspondiente a cero
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                FROG_SPEEDS[0] = 0
            elif event.key == pygame.K_RIGHT:
                FROG_SPEEDS[1] = 0
            elif event.key == pygame.K_UP:
                FROG_SPEEDS[2] = 0
            elif event.key == pygame.K_DOWN:
                FROG_SPEEDS[3] = 0

    # Calcular la posición de la rana en cada cuadro
    FROG_X += (FROG_SPEEDS[1] + FROG_SPEEDS[0]) / 60
    FROG_Y += (FROG_SPEEDS[3] + FROG_SPEEDS[2]) / 60

    # Limitar la posición de la rana a la banda horizontal
    if FROG_X < 0:
        FROG_X = 0
    elif FROG_X > SCREEN_WIDTH - FROG_SIZE[0]:
        FROG_X = SCREEN_WIDTH - FROG_SIZE[0]
    if FROG_Y < BAND_TOP:
        FROG_Y = BAND_TOP
    elif FROG_Y > SCREEN_HEIGHT - FROG_SIZE[1]:
        FROG_Y = SCREEN_HEIGHT - FROG_SIZE[1]

    # Dibujar capa de fondo
    screen.blit(background_surface, (0, 0))

    # Dibujar la banda horizontal
    pygame.draw.rect(screen, BAND_COLOR, (BAND_LEFT, BAND_TOP, BAND_WIDTH, BAND_HEIGHT))

    # Dibujar la imagen de la rana en la pantalla
    screen.blit(frog_image, (FROG_X, FROG_Y))

    # Actualizar la pantalla
    pygame.display.update()

