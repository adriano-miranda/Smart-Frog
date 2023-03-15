import pygame

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Inicializar Pygame
pygame.init()

# Definir la pantalla
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ejemplo de temporizador")

# Definir el temporizador
tiempo_total = 5000  # 5 segundos
tiempo_restante = tiempo_total
temporizador_activado = False

# Definir el objeto
objeto_rect = pygame.Rect(350, 250, 100, 100)
objeto_activo = False

# Definir el reloj
reloj = pygame.time.Clock()
jugador_rect = pygame.Rect(350, 250, 50, 50)

# Loop principal del juego
while True:
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Si el jugador colisiona con el objeto, activar el temporizador
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE and not objeto_activo:
            if objeto_rect.colliderect(jugador_rect):
                temporizador_activado = True
                objeto_activo = True

    # Actualizar el temporizador si está activado
    if temporizador_activado:
        tiempo_restante -= reloj.tick(60)  # Descontar tiempo del reloj
        if tiempo_restante <= 0:
            tiempo_restante = tiempo_total
            temporizador_activado = False
            objeto_activo = False

    # Limpiar la pantalla
    pantalla.fill(BLANCO)

    # Dibujar el objeto si está activo
    if objeto_activo:
        pygame.draw.rect(pantalla, NEGRO, objeto_rect)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar el tiempo de actualización de la pantalla
    reloj.tick(60)
 
