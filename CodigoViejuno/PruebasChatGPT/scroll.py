import pygame

pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Configuración del jugador
player_size = 50
player = pygame.Rect(SCREEN_WIDTH//2 - player_size//2, SCREEN_HEIGHT//2 - player_size//2, player_size, player_size)
player_speed = 5

# Configuración del scroll vertical
scroll_speed = 3
scroll_top = 0
scroll_bottom = SCREEN_HEIGHT

# Bucle principal
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move_ip(0, -player_speed)
            elif event.key == pygame.K_DOWN:
                player.move_ip(0, player_speed)

    # Actualización de la posición del jugador
    if player.top < scroll_top:
        player.top = scroll_top
    elif player.bottom > scroll_bottom:
        player.bottom = scroll_bottom

    # Actualización del scroll vertical
    if player.top < scroll_top + SCREEN_HEIGHT//4:
        scroll_top -= scroll_speed
        scroll_bottom -= scroll_speed
    elif player.bottom > scroll_bottom - SCREEN_HEIGHT//4:
        scroll_top += scroll_speed
        scroll_bottom += scroll_speed
        
    print(scroll_top, " ", scroll_bottom)

    # Pintado de la pantalla
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), player.move(0, -scroll_top))
    pygame.display.flip()

pygame.quit()
