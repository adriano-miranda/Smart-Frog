import pygame

pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Definir dimensiones de la pantalla
ANCHO_PANTALLA = 640
ALTO_PANTALLA = 480
DIMENSIONES_PANTALLA = (ANCHO_PANTALLA, ALTO_PANTALLA)

# Crear pantalla
pantalla = pygame.display.set_mode(DIMENSIONES_PANTALLA)

# Definir fuente
fuente = pygame.font.SysFont("calibri", 20)

# Definir texto
texto = fuente.render("¡Hola, mundo!", True, BLANCO)

# Definir posición del texto
posicion_texto = [ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2]

# Definir posición del puntero
posicion_puntero = ALTO_PANTALLA // 2

# Definir posición del scroll
posicion_scroll = 0

# Definir velocidad del scroll
velocidad_scroll = 5

# Loop principal del juego
while True:

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 4:
                posicion_scroll += velocidad_scroll
            elif evento.button == 5:
                posicion_scroll -= velocidad_scroll

    # Obtener posición del puntero
    posicion_puntero = pygame.mouse.get_pos()[1]

    # Calcular posición del texto teniendo en cuenta la posición del scroll
    posicion_texto[1] = (ALTO_PANTALLA // 2) - posicion_scroll

    # Calcular posición del puntero teniendo en cuenta la posición del scroll
    posicion_puntero -= posicion_scroll

    # Limpiar pantalla
    pantalla.fill(NEGRO)

    # Dibujar texto en pantalla
    pantalla.blit(texto, (posicion_texto[0] - texto.get_width() // 2, posicion_texto[1]))

    # Dibujar puntero en pantalla
    pygame.draw.line(pantalla, BLANCO, (0, posicion_puntero), (ANCHO_PANTALLA, posicion_puntero))

    # Actualizar pantalla
    pygame.display.update() 
