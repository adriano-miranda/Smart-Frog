import pygame
from pygame import *
import sys, os

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Crear la ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Establecer el título de la ventana
pygame.display.set_caption("Smart Frog")

while True:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclado = key.get_pressed()
    print("Derecha: " + bool.__str__(teclado[K_RIGHT]))
    print("Izquierda: " + bool.__str__(teclado[K_LEFT]))
    print("Arriba: " + bool.__str__(teclado[K_UP]))
    print("Abajo: " + bool.__str__(teclado[K_DOWN]))
    print("Salto: " + bool.__str__(teclado[K_SPACE]))
    time.delay(500)
    print("\n\n\n\n\n")

    # Actualizar la pantalla
    pygame.display.update()
